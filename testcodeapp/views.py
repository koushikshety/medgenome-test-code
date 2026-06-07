from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Category, Document, TestCode, PreData, Log, UploadedFile, LockCode


def index_view(request):
    return render(request, 'index.html')


@csrf_exempt
@require_http_methods(["GET", "POST"])
def categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return JsonResponse({'categories': [cat.name for cat in categories]})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        category, created = Category.objects.get_or_create(name=data['name'])
        Log.objects.create(message=f"Category {'created' if created else 'already exists'}: {data['name']}")
        return JsonResponse({'success': True, 'category': category.name})


@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def category_detail(request, name):
    try:
        category = Category.objects.get(name=name)
    except Category.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Category not found'}, status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        old_name = category.name
        category.name = data['new_name']
        category.save()
        Log.objects.create(message=f"Category updated: {old_name} -> {data['new_name']}")
        return JsonResponse({'success': True})
    
    elif request.method == 'DELETE':
        category.delete()
        Log.objects.create(message=f"Category deleted: {name}")
        return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def documents(request):
    if request.method == 'GET':
        docs = Document.objects.all()
        return JsonResponse({'documents': [doc.name for doc in docs]})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        doc, created = Document.objects.get_or_create(name=data['name'])
        Log.objects.create(message=f"Document {'created' if created else 'already exists'}: {data['name']}")
        return JsonResponse({'success': True, 'document': doc.name})


@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def document_detail(request, name):
    try:
        doc = Document.objects.get(name=name)
    except Document.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Document not found'}, status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        old_name = doc.name
        doc.name = data['new_name']
        doc.save()
        Log.objects.create(message=f"Document updated: {old_name} -> {data['new_name']}")
        return JsonResponse({'success': True})
    
    elif request.method == 'DELETE':
        doc.delete()
        Log.objects.create(message=f"Document deleted: {name}")
        return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def test_codes(request):
    if request.method == 'GET':
        test_codes = TestCode.objects.all()
        result = []
        for tc in test_codes:
            doc_names = [d.name for d in tc.documents.all()]
            result.append({
                'id': tc.id,
                'mgmCode': tc.mgm_code,
                'category': tc.category.name,
                'status': tc.status,
                'documents': ', '.join(doc_names)
            })
        return JsonResponse({'testCodes': result})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            category = Category.objects.get(name=data['category'])
            tc = TestCode.objects.create(
                mgm_code=data['mgmCode'],
                category=category,
                status=data['status']
            )
            if data.get('documents'):
                doc = Document.objects.get(name=data['documents'])
                tc.documents.add(doc)
            Log.objects.create(message=f"Test code created: {data['mgmCode']}")
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def test_code_detail(request, mgm_code):
    try:
        tc = TestCode.objects.get(mgm_code=mgm_code)
    except TestCode.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Test code not found'}, status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            tc.category = Category.objects.get(name=data['category'])
            tc.status = data['status']
            tc.documents.clear()
            if data.get('documents'):
                doc_names = [d.strip() for d in data['documents'].split(',') if d.strip()]
                for doc_name in doc_names:
                    doc, _ = Document.objects.get_or_create(name=doc_name)
                    tc.documents.add(doc)
            tc.save()
            Log.objects.create(message=f"Test code updated: {mgm_code}")
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        tc.delete()
        Log.objects.create(message=f"Test code deleted: {mgm_code}")
        return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def pre_data(request):
    if request.method == 'GET':
        pre_data_list = PreData.objects.all()
        result = []
        for pd in pre_data_list:
            doc_names = [d.name for d in pd.documents.all()]
            result.append({
                'id': pd.id,
                'mgmCode': pd.mgm_code,
                'category': pd.category.name,
                'status': pd.status,
                'documents': ', '.join(doc_names)
            })
        return JsonResponse({'preData': result})
    
    elif request.method == 'POST':
        data_list = json.loads(request.body)
        for data in data_list:
            try:
                category = Category.objects.get(name=data['category'])
                pd = PreData.objects.create(
                    mgm_code=data['mgmCode'],
                    category=category,
                    status=data['status']
                )
                Log.objects.create(message=f"Pre data created: {data['mgmCode']}")
            except Exception as e:
                pass
        return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["DELETE"])
def pre_data_detail(request, id):
    try:
        pd = PreData.objects.get(id=id)
    except PreData.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pre data not found'}, status=404)
    
    pd.delete()
    Log.objects.create(message=f"Pre data deleted: {pd.mgm_code}")
    return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["POST"])
def approve_pre_data(request):
    data = json.loads(request.body)
    pre_data_ids = data.get('ids', [])
    
    for pd_id in pre_data_ids:
        try:
            pd = PreData.objects.get(id=pd_id)
            tc, created = TestCode.objects.get_or_create(
                mgm_code=pd.mgm_code,
                defaults={'category': pd.category, 'status': pd.status}
            )
            if not created:
                tc.category = pd.category
                tc.status = pd.status
                tc.save()
            tc.documents.set(pd.documents.all())
            pd.delete()
            Log.objects.create(message=f"Pre data approved: {pd.mgm_code}")
        except Exception as e:
            pass
    
    return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_all_pre_data(request):
    PreData.objects.all().delete()
    Log.objects.create(message="All pre data deleted")
    return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["GET"])
def logs(request):
    log_list = Log.objects.all().order_by('-timestamp')
    result = []
    for log in log_list:
        result.append({
            'timestamp': log.timestamp.isoformat(),
            'displayTimestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'message': log.message
        })
    return JsonResponse({'logs': result})


@csrf_exempt
@require_http_methods(["DELETE"])
def clear_logs(request):
    Log.objects.all().delete()
    return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_last_week_logs(request):
    from datetime import timedelta
    from django.utils import timezone
    one_week_ago = timezone.now() - timedelta(weeks=1)
    Log.objects.filter(timestamp__lt=one_week_ago).delete()
    Log.objects.create(message="Last week's logs deleted")
    return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def lock_code(request):
    if request.method == 'GET':
        lock_code_obj, created = LockCode.objects.get_or_create(id=1)
        return JsonResponse({'lockCode': lock_code_obj.code})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        lock_code_obj, created = LockCode.objects.get_or_create(id=1)
        lock_code_obj.code = data['newCode']
        lock_code_obj.save()
        Log.objects.create(message="Lock code changed")
        return JsonResponse({'success': True})
