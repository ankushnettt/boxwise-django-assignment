def fits_in_box(product, box):
    product_dims = sorted([product.length, product.width, product.height])
    box_dims = sorted([box.length, box.width, box.height])
    return all(p <= b for p, b in zip(product_dims, box_dims))
