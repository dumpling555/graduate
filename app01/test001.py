list=[{'tid': 1, 'name': '刘玉杰', 'class_name': '电科技161'},
{'tid': 1, 'name': '刘玉杰', 'class_name': '电科技162'},
{'tid': 1, 'name': '刘玉杰', 'class_name': '通信161'},
{'tid': 2, 'name': '梁瑞宇', 'class_name': '电科技161'},
{'tid': 2, 'name': '梁瑞宇', 'class_name': '电科技162'},
{'tid': 2, 'name': '梁瑞宇', 'class_name': '计科技161'},
{'tid': 3, 'name': '潘子宇', 'class_name': '电信161'},
{'tid': 4, 'name': '唐晓雨', 'class_name': '电信161'},
{'tid': 5, 'name': '冯月芹', 'class_name': '电信161'}]

result={ }
for row in list:

    tid=row['tid']
    if tid in result:
        result[tid]['titles'].append(row['class_name'])
    else:
        result[tid]={'tid':row['tid'],'name':row['name'],'titles':[row['class_name'],]}
print(result)
