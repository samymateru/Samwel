data = {
  "lod1_owner": [
    {
      "name": "sam",
      "email": "samymateru@gmail.com",
      "date_issued": "2025-05-19T06:21:07.148000+00:00"
    },
    {
        "name": "bonny",
        "email": "bonnyu@gmail.com",
        "date_issued": "2025-05-19T06:21:07.148000+00:00"
    }
  ],
}

owners = [f"{owner['name']}, {owner['email']}" for owner in data.get("lod1_owner", [])]


formatted_data = {
    "lod1_owner": owners
}

print(formatted_data)