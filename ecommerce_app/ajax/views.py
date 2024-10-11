from django.http.response import JsonResponse
from ..models import Order, Transaction



def update_order_status(request):
    order_id = request.POST.get('order_id')
    new_status = request.POST.get('new_status')
    try:
        user = Order.objects.get(pk=order_id)
        user.status = new_status
        user.save()
        return JsonResponse({'success': True})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'})



def update_tnx_status(request):
    tnx_id = request.POST.get('tnx_id')
    new_status = request.POST.get('new_status')
    try:
        user = Transaction.objects.get(pk=tnx_id)
        user.status = new_status
        user.save()
        return JsonResponse({'success': True})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Transaction not found'})
