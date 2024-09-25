def test_create_product(test_client):
    response = test_client.post("/api/v1/products", json={
        "name": "string",
        "desc": "string",
        "price": 0,
        "stock": 5
    })
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "string", "desc": "string", "price": 0, "stock": 5}

    response = test_client.post("/api/v1/products", json={
        "name": "string1",
        "desc": "string",
        "price": 0,
        "stock": 5
    })
    assert response.status_code == 200
    assert response.json() == {"id": 2, "name": "string1", "desc": "string", "price": 0, "stock": 5}

    response = test_client.post("/api/v1/products", json={
        "name": "string",
        "desc": "string",
        "price": 0,
        "stock": 0
    })
    assert response.status_code == 422
    assert response.json() == {"detail": "Product already exists"}

def test_get_all_products(test_client):
    response = test_client.get("/api/v1/products")
    assert response.status_code == 200
    assert response.json() == {"products": [{"id": 1, "name": "string", "desc": "string", "price": 0, "stock": 5},
                                            {"id": 2, "name": "string1", "desc": "string", "price": 0, "stock": 5}]}

def test_get_product_info(test_client):
    response = test_client.get("/api/v1/products/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "string", "desc": "string", "price": 0, "stock": 5}

    response = test_client.get("/api/v1/products/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid product id"}

def test_delete_product(test_client):
    response = test_client.delete("/api/v1/products/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Product 1 successfully deleted."}

    response = test_client.get("/api/v1/products/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid product id"}
