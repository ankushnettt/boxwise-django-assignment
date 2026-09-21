from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Order


def recommend_box_view(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

    box = order.recommend_box()

    if box is None:
        return JsonResponse(
            {
                "order": order.pk,
                "recommended_box": None,
                "message": "No suitable box found",
            }
        )

    return JsonResponse(
        {
            "order": order.pk,
            "recommended_box": {
                "name": box.name,
                "length": box.length,
                "width": box.width,
                "height": box.height,
                "max_weight": box.max_weight,
                "cost": box.cost,
            },
        }
    )


def recommend_box_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        "order": order,
        "recommended_box": order.recommend_box(),
    }
    return render(request, "boxes/result.html", context)
