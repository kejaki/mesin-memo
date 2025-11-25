from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import ContentItem, ContentComment, ActivityLog, JobRole, JobRoleAssignment, Status
from .forms import ContentItemForm, ContentCommentForm, JobRoleFormSet

@login_required
def create_content(request):
    if request.method == 'POST':
        form = ContentItemForm(request.POST)
        formset = JobRoleFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            content = form.save(commit=False)
            content.author = request.user
            content.status = Status.IDEA
            content.save()
            
            # Save job roles
            formset.instance = content
            formset.save()
            
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                action=ActivityLog.Action.CREATED,
                content=content,
                description=f"Membuat konten '{content.title}'"
            )
            
            messages.success(request, 'Konten berhasil dibuat!')
            return redirect('cms_dashboard')
    else:
        form = ContentItemForm()
        formset = JobRoleFormSet()
    
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'cms/create_content.html', context)

@login_required
def edit_content(request, content_id):
    """Edit existing content with job roles"""
    content = get_object_or_404(ContentItem, id=content_id)
    
    # Check permission (only author or staff can edit)
    if content.author != request.user and not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki izin untuk mengedit konten ini.')
        return redirect('content_detail', content_id=content_id)
    
    if request.method == 'POST':
        form = ContentItemForm(request.POST, instance=content)
        formset = JobRoleFormSet(request.POST, instance=content)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            messages.success(request, 'Konten berhasil diupdate!')
            return redirect('content_detail', content_id=content_id)
    else:
        form = ContentItemForm(instance=content)
        formset = JobRoleFormSet(instance=content)
    
    context = {
        'form': form,
        'formset': formset,
        'content': content,
        'is_edit': True,
    }
    return render(request, 'cms/create_content.html', context)

@login_required
def delete_content(request, content_id):
    """Delete content"""
    content = get_object_or_404(ContentItem, id=content_id)
    
    # Check permission
    if content.author != request.user and not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki izin untuk menghapus konten ini.')
        return redirect('content_detail', content_id=content_id)
    
    if request.method == 'POST':
        title = content.title
        content.delete()
        messages.success(request, f'Konten "{title}" berhasil dihapus.')
        return redirect('cms_dashboard')
    
    return render(request, 'cms/delete_confirm.html', {'content': content})

@login_required
def manage_content(request):
    """Admin-like content management view"""
    if not request.user.is_staff:
        messages.error(request, 'Akses ditolak. Hanya untuk admin.')
        return redirect('cms_dashboard')
    
    contents = ContentItem.objects.all().select_related('author', 'claimed_by').prefetch_related('job_roles').order_by('-created_at')
    
    # Filter
    status_filter = request.GET.get('status', '')
    if status_filter:
        contents = contents.filter(status=status_filter)
    
    search = request.GET.get('search', '')
    if search:
        contents = contents.filter(Q(title__icontains=search) | Q(description__icontains=search))
    
    context = {
        'contents': contents,
        'status_choices': Status.choices,
        'current_status': status_filter,
        'search_query': search,
    }
    return render(request, 'cms/manage_content.html', context)

@login_required
def update_content_status(request, content_id):
    """Quick status update via AJAX"""
    content = get_object_or_404(ContentItem, id=content_id)
    
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Status.choices).keys():
            content.status = new_status
            content.save()
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
def dashboard(request):
    # Get all content items ordered by target date
    contents = ContentItem.objects.all().prefetch_related('job_roles__assignments').order_by('target_date')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        contents = contents.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        contents = contents.filter(status=status_filter)
    
    # Simple grouping by status for Kanban-like view
    ideas = contents.filter(status=Status.IDEA)
    in_progress = contents.filter(status=Status.IN_PROGRESS)
    review = contents.filter(status=Status.REVIEW)
    final = contents.filter(status=Status.FINAL)
    uploaded = contents.filter(status=Status.UPLOADED)
    
    context = {
        'ideas': ideas,
        'in_progress': in_progress,
        'review': review,
        'final': final,
        'uploaded': uploaded,
        'search_query': search_query,
    }
    return render(request, 'cms/dashboard.html', context)

@login_required
def available_jobs(request):
    """List all content with available job roles"""
    # Get content that has job roles with available slots
    contents = ContentItem.objects.filter(
        is_claimable=True,
        job_roles__isnull=False
    ).prefetch_related('job_roles__assignments').distinct().order_by('target_date')
    
    # Filter to only show content with at least one available role
    available_contents = []
    for content in contents:
        has_available_role = any(not role.is_full() for role in content.job_roles.all())
        if has_available_role:
            available_contents.append(content)
    
    context = {
        'contents': available_contents,
    }
    return render(request, 'cms/available_jobs.html', context)

@login_required
def my_jobs(request):
    """List all jobs claimed by current user"""
    # Get jobs where user has claimed a role
    role_assignments = JobRoleAssignment.objects.filter(
        user=request.user
    ).select_related('job_role__content').order_by('-assigned_at')
    
    context = {
        'assignments': role_assignments,
    }
    return render(request, 'cms/my_jobs.html', context)

@login_required
def claim_job(request, content_id):
    """Legacy: Claim entire job (kept for backward compatibility)"""
    content = get_object_or_404(ContentItem, id=content_id)
    
    # Check if already claimed
    if content.claimed_by is not None:
        messages.error(request, 'Job ini sudah diambil oleh orang lain.')
        return redirect('available_jobs')
    
    # Check if claimable
    if not content.is_claimable:
        messages.error(request, 'Job ini tidak bisa diambil.')
        return redirect('available_jobs')
    
    # Claim the job
    content.claimed_by = request.user
    content.claimed_at = timezone.now()
    content.status = Status.IN_PROGRESS
    
    # Auto-assign as author if not assigned
    if not content.author:
        content.author = request.user
    
    content.save()
    
    # Log activity
    ActivityLog.objects.create(
        user=request.user,
        action=ActivityLog.Action.CLAIMED,
        content=content,
        description=f"Mengambil job '{content.title}'"
    )
    
    messages.success(request, f'Berhasil mengambil job "{content.title}"!')
    return redirect('my_jobs')

@login_required
def unclaim_job(request, content_id):
    """Release a claimed job (only if IN_PROGRESS)"""
    content = get_object_or_404(ContentItem, id=content_id, claimed_by=request.user)
    
    # Only allow unclaim if still in progress
    if content.status != Status.IN_PROGRESS:
        messages.error(request, 'Tidak bisa melepas job yang sudah dalam review/final.')
        return redirect('my_jobs')
    
    content.claimed_by = None
    content.claimed_at = None
    content.status = Status.IDEA
    content.save()
    
    messages.success(request, f'Job "{content.title}" berhasil dilepas.')
    return redirect('available_jobs')

@login_required
def content_detail(request, content_id):
    """Detail page for content with comments and job roles"""
    content = get_object_or_404(ContentItem, id=content_id)
    comments = content.comments.all()
    job_roles = content.job_roles.prefetch_related('assignments__user').all()
    
    # Check which roles user has claimed
    user_assignments = JobRoleAssignment.objects.filter(
        job_role__content=content,
        user=request.user
    ).values_list('job_role_id', flat=True)
    
    if request.method == 'POST':
        form = ContentCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content = content
            comment.user = request.user
            comment.save()
            
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                action=ActivityLog.Action.COMMENTED,
                content=content,
                description=f"Berkomentar di '{content.title}'"
            )
            
            messages.success(request, 'Komentar berhasil ditambahkan!')
            return redirect('content_detail', content_id=content_id)
    else:
        form = ContentCommentForm()
    
    context = {
        'content': content,
        'comments': comments,
        'job_roles': job_roles,
        'user_assignments': list(user_assignments),
        'form': form,
    }
    return render(request, 'cms/content_detail.html', context)

@login_required
def claim_role(request, role_id):
    """Claim a specific job role"""
    job_role = get_object_or_404(JobRole, id=role_id)
    
    # Check if user already has ANY role in this content
    existing_role = JobRoleAssignment.objects.filter(
        job_role__content=job_role.content,
        user=request.user
    ).first()
    
    if existing_role:
        messages.error(
            request, 
            f'Anda sudah mengambil role {existing_role.job_role.get_role_type_display()} di konten ini. '
            'Hanya bisa ambil 1 role per konten.'
        )
        return redirect('content_detail', content_id=job_role.content.id)
    
    # Check if role is full
    if job_role.is_full():
        messages.error(request, f'Role {job_role.get_role_type_display()} sudah penuh.')
        return redirect('content_detail', content_id=job_role.content.id)
    
    # Create assignment
    JobRoleAssignment.objects.create(
        job_role=job_role,
        user=request.user
    )
    
    # Log activity
    ActivityLog.objects.create(
        user=request.user,
        action=ActivityLog.Action.CLAIMED_ROLE,
        content=job_role.content,
        description=f"Mengambil role {job_role.get_role_type_display()} di '{job_role.content.title}'"
    )
    
    messages.success(request, f'Berhasil mengambil role {job_role.get_role_type_display()}!')
    return redirect('content_detail', content_id=job_role.content.id)

@login_required
def unclaim_role(request, assignment_id):
    """Release a claimed role"""
    assignment = get_object_or_404(JobRoleAssignment, id=assignment_id, user=request.user)
    content_id = assignment.job_role.content.id
    role_name = assignment.job_role.get_role_type_display()
    
    # Check if content is already uploaded
    if assignment.job_role.content.status == Status.UPLOADED:
        messages.error(request, 'Tidak bisa melepas role dari konten yang sudah uploaded.')
        return redirect('content_detail', content_id=content_id)
    
    assignment.delete()
    
    messages.success(request, f'Role {role_name} berhasil dilepas.')
    return redirect('content_detail', content_id=content_id)
