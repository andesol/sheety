# Sheety

! In development

A minimal library to save and retrieve data on Google Sheets, using DjangoORM-like syntax

## Documentation

### Usage

```py
import sheety

s = sheety.build(spreadsheet_id=XXX, service_account_info=...)

@s.model(name="blogs")
blog = Blog(
    id=1,
    title="First post",
    content="This is my first post"
)

blog.save()
```

### Update data

```py
first_post.title = "Python is good!"

first.save()
```

### Get one

```py
post = Blog.objects.get(id=1)

print(blog.title)
# Python is good!
```

### Get all

```py
post = Blog.objects.all()

print(blog.title)
```

### Filter

```py
post = Blog.objects.filter(id=1)

print(blog.title)
# Python is good!
```
