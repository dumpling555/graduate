import pymysql
import json
from django.shortcuts import render, HttpResponse, redirect
from utils import sqlhelper


# 装饰器
def auth(func):
    def wrapper(request, *args, **kwargs):
        if request.COOKIES:
            return func(request, *args, **kwargs)
        return redirect('/login/')

    return wrapper


@auth
def classes(request):
    # connect
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dangdang')
    cursor = conn.cursor()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 设置查询结果为字典格式
    cursor.execute("select id,class_name from class")
    class_list = cursor.fetchall()  # 结果为字典
    cursor.close()
    conn.close()

    return render(request, 'classes.html', {'class_list': class_list})


@auth
def add(request):
    if request.method == 'GET':
        return render(request, 'add.html')
    else:

        v = request.POST.get('class_name')
        if (len(v) > 0):
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dangdang')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute("insert into class(class_name) value(%s)", [v, ])
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/classes/')
        else:
            return render(request, 'add.html', {'msg': '班级名称不能为空'})


@auth
def delete(request):
    # if request.method=='GET':
    #     return render(request,'delete.html')
    # else:
    print('==============')
    print(request.GET)
    delete_id = request.GET.get('id')
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='dangdang')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from class where id=%s", [delete_id, ])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/classes/')


@auth
def edit(request):
    """
    #这一段主要是为了在跳转的页面上显示原始数据
    先找到指定id的值，再拿出来，显示到浏览器上
    sql语句是：select xxx from xxx where xxx
    :param request:
    :return:
    """
    if request.method == 'GET':
        # return render(request,'edit.html')
        # print('|-----------以下是get-----------------|')
        # print(request.__dict__)
        edit_id = request.GET.get('id')
        edit_name = request.GET.get('class_name')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dangdang')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,class_name from class where id=%s", [edit_id, ])
        result = cursor.fetchone()
        # print(result)
        cursor.close()
        conn.close()
        return render(request, 'edit.html', {'result': result})
    else:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dangdang')
        edit_id = request.GET.get('id')
        edit_name = request.POST.get('class_name')
        # print('|-----------以下是post-----------------|')
        # print(request.__dict__)
        # print(edit_name, edit_id)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update class set class_name=%s where id=%s", [edit_name, edit_id, ])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/classes/')


@auth
def student_manage(request):
    """

    :param request:
    :return:
    """
    delete_id = request.GET.get('id')
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='dangdang')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT student.id,student.`name`,student.classid,class.class_name FROM student LEFT JOIN class on  student.classid=class.id")
    student_list = cursor.fetchall()
    # cursor.execute("select course.course_name,course.time,teacher.name,course.credit from course,teacher,course_student,student where  course_student.course_number=course.course_number and course.student=studnet.id and course.teacher_name=teracher.id ")
    cursor.close()
    conn.close()
    class_list = sqlhelper.getall('select id,class_name from class ', [])
    print(student_list)
    return render(request, 'student_manage.html', {'student_list': student_list, 'class_list': class_list})


@auth
def student_add(request):
    if request.method == 'GET':
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='dangdang')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,class_name from class ")
        class_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render(request, 'student_add.html', {'class_list': class_list})
    else:
        classid = request.POST.get('class_id')
        student_name = request.POST.get('name')
        print(classid)

        # cursor.execute("insert into student(`name`,classid)")
        # conn.commit()
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='dangdang')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute("insert into student(`name`,classid)values(%s,%s)", [student_name, classid, ])
        cursor.fetchone()
        cursor.close()
        conn.close()

        # student_list = cursor.fetchall()

        return redirect('/student_manage/')


@auth
def student_edit(request):
    if request.method == 'GET':
        # return render(request,'edit.html')
        print('|-----------以下是get-----------------|')
        print(request.__dict__)
        # global student_edit_id
        student_edit_id = request.GET.get('id')  # 这个id来自于html中，使用get
        print(student_edit_id)
        student_edit_name = request.GET.get('class_name')
        current_student_info = sqlhelper.getone("select id,`name`,classid from student where id=%s",
                                                [student_edit_id, ])
        # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dangdang')
        # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # cursor.execute("select `name`,classid from student where id=%s", [student_edit_id, ])
        #
        # #把student中的一条选中，发到html中
        # """
        #  result name,classid
        # """
        # result=cursor.fetchone()
        print(current_student_info)
        # cursor.execute("select id,class_name from class")
        # class_list = cursor.fetchall()
        # cursor.close()
        # conn.close()
        class_list = sqlhelper.getall("select id,class_name from class", [])
        return render(request, 'student_edit.html',
                      {'current_student_info': current_student_info, 'class_list': class_list,
                       'student_id': student_edit_id})
    else:
        student_edit_id = request.GET.get('id')  # 学号,也就是学生的唯一id
        student_edit_classid = request.POST.get('classid')
        student_edit_name = request.POST.get('student_name')
        print('|-----------以下是post-----------------|')
        print(student_edit_classid, student_edit_name, student_edit_id)
        print(request.__dict__)
        sqlhelper.modify('update student set `name`=%s,classid=%s where id=%s',
                         [student_edit_name, student_edit_classid, student_edit_id, ])

        # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dangdang')
        # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        #
        # cursor.execute("update student set `name`=%s,classid=%s where id=%s", [student_edit_name, student_edit_classid ,student_edit_id, ])
        # print('===================')
        # conn.commit()
        # cursor.close()
        # conn.close()
        return redirect('/student_manage/')


@auth
def modal_add_class(request):
    # class_name=request.POST.get('class_name')
    # msg='班级不能为空空哦'
    # if(len(class_name)>0):
    #     sqlhelper.modify('insert into class(class_name)values(%s)',[class_name,])
    #     return redirect('/classes/')
    # else:
    #     #
    #     return render(request,'classes.html',{'msg':msg})
    class_name = request.POST.get('class_name')
    if len(class_name) > 0:
        print('=====等待插入=========')
        sqlhelper.modify('insert into class (class_name)value(%s)', [class_name, ])
        return HttpResponse('ok')
        print('=====插入成功=========')
        return redirect('/classes/')
    else:
        return HttpResponse('班级标题不能为空')


@auth
def modal_del_class(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        print('接收到', nid)
        content = request.POST.get('content')
        print('准备删除======================')
        sqlhelper.modify('delete from class where id=%s', [nid, ])
        print('删除成功====================')
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    import json
    return HttpResponse(json.dumps(ret))  # 使用json将字典转变成字符串


@auth
def modal_edit_class(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        content = request.POST.get('content')
        sqlhelper.modify('update class set class_name=%s where id=%s', [content, nid])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    import json
    return HttpResponse(json.dumps(ret))  # 使用json将字典转变成字符串


@auth
def modal_add_student(request):
    ret = {'status': True, 'message': None}
    name = request.POST.get('name')
    class_id = request.POST.get('class_id')
    # try:
    #     if(len(name)>0):
    #         sqlhelper.modify('insert into student(name,classid)values (%s,%s)',[name,class_id])
    #     else:
    # except Exception as e:
    #     ret['status']=False
    #     ret['message']=str(e)
    # return  HttpResponse(json.dumps(ret))
    if (len(name) > 0):
        sqlhelper.modify('insert into student(name,classid)values (%s,%s)', [name, class_id])
        return HttpResponse('ok')
    else:
        return HttpResponse('error')


@auth
def modal_edit_student(request):
    # 'student_id':$('#edit_student_id').val(),
    # 'class_id':$('#edit_class_id').val(),
    # 'student_name':$('#edit_name').val},
    student_id = request.POST.get('student_id')
    class_id = request.POST.get('class_id')
    student_name = request.POST.get('student_name')
    print(student_name, student_id, class_id)
    sqlhelper.modify('update student set `name`=%s,classid=%s where id=%s', [student_name, class_id, student_id, ])
    print('=================okk=====================')
    return HttpResponse('okk')  # 这一步非常重要，告诉前端，你好了


@auth
def modal_del_student(request):
    student_id = request.POST.get('student_id')
    class_id = request.POST.get('class_id')
    student_name = request.POST.get('student_name')
    print('+++++++*****已获取身份******++++++')
    print(student_name, student_id, class_id)
    sqlhelper.modify('delete from student where id=%s', [student_id, ])
    return HttpResponse('ok')


@auth
def teacher(request):
    sql = """
        
    SELECT teacher.id as tid,teacher.name, class.class_name FROM teacher

LEFT JOIN teacher_class on teacher.id=teacher_class.teacher_id
LEFT JOIN class on class.id=teacher_class.class_id
    
    """
    teacher_list = sqlhelper.getall(sql, [])
    print(teacher_list)
    result = {}
    for row in teacher_list:

        tid = row['tid']
        if tid in result:
            result[tid]['titles'].append(row['class_name'])
        else:
            result[tid] = {'tid': row['tid'], 'name': row['name'], 'titles': [row['class_name'], ]}
    # print(result)
    return render(request, 'teacher.html', {'teacher_list': result.values()})

@auth
def del_teacher(request):
    if request.method=='POST':
        del_teacher_id=request.POST.get('nid')
        related_class=request.POST.get
        print('===================',del_teacher_id)
        sql_teacher="""
        delete from teacher where id=%s;
        """
        sql_teacher2class="""
        delete from teacher_class where teacher_id=%s
        """
        obj = sqlhelper.SqlHelper()
        obj.modify(sql_teacher, [del_teacher_id])
        obj.modify(sql_teacher2class,[del_teacher_id])
        return redirect('/teacher/')
    else:
        return redirect('/teacher/')

@auth
def add_teacher(request):
    if request.method == 'GET':
        class_list = sqlhelper.getall('select id,class_name from class', [])
        return render(request, 'add_teacher.html', {'class_list': class_list})
    else:
        data_list = []
        name = request.POST.get('name')
        class_ids = request.POST.getlist('class_id')
        print(name, class_ids)
        obj = sqlhelper.SqlHelper()
        # 老师表中添加一条数据
        teacher_id = obj.create('insert into teacher(name)value(%s)', [name, ])  # create has return value
        for item in class_ids:
            temp = (teacher_id, item,)
            data_list.append(temp)
        obj.multiple_modify('insert into teacher_class(teacher_id,class_id)values (%s,%s)', data_list)
        return redirect('/teacher/')


@auth
def edit_teacher(request):
    if request.method == 'GET':
        obj = sqlhelper.SqlHelper()
        current_teacher_id = request.GET.get('nid')
        print(current_teacher_id)

        # 班级列表
        class_list = obj.getall('select id,class_name from class', [])
        # 当前教师信息
        current_teacher_info = obj.getone('select id,name from teacher where id=%s', [current_teacher_id, ])
        # 老师-班级关系
        class_id_list = obj.getall('select class_id from teacher_class where teacher_id=%s', [current_teacher_id, ])

        print('当前老师任教的班级id', class_id_list)

        print('当前老师信息', current_teacher_info)
        print('班级列表', class_list)
        temp = []
        for i in class_id_list:
            temp.append(i['class_id'])
        print(temp)
        return render(request, 'edit_teacher.html',
                      {'class_list': class_list, 'info': current_teacher_info, 'class_id_list': temp})
    else:
        data_list = []
        teacher_id = request.GET.get('nid')
        teacher_name = request.POST.get('name')
        class_id = request.POST.getlist('class_id')
        print('teacher id', teacher_id)
        print('teacher_name', teacher_name)
        print('classid', class_id)
        obj = sqlhelper.SqlHelper()
        obj.modify('update teacher set name=%s where id=%s', [teacher_name, teacher_id])
        obj.modify('delete from teacher_class where teacher_id=%s', [teacher_id, ])
        for item in class_id:
            temp = (teacher_id, item,)
            data_list.append(temp)
        obj = sqlhelper.SqlHelper()
        obj.multiple_modify('insert into teacher_class(teacher_id,class_id)values (%s,%s)', data_list)
        obj.close()

        return redirect('/teacher/')


@auth
def layout(request):
    obj = render(request, 'layout.html')
    return obj

@auth
def select_course(request):

    sql="""
    SELECT
	course.course_name,
	course.time,
	teacher.name,
	course.credit,
	course.course_number
FROM
	course,
	teacher,
	course_student,
	student 
WHERE
	course_student.course_number = course.course_number 
	AND course_student.student = student.id 
	AND course.teacher_name = teacher.id
	and course_student.student=%s
    
    
    """

    sql_student="select course_number from course_student where student=%s "

    sql_course="select course_number from course "

    obj = sqlhelper.SqlHelper()
    if request.method == 'GET':
        #这里有个问题，就是全局变量username会失灵，改成g_username就没事了，纯bug
        course_list = obj.getall(sql, [g_username,])

        print('course_list',course_list)

        user=obj.getone('select name from student where id = %s',[username,])
        student_selected_course=obj.getall(sql_student,[username,])
        all_course=obj.getall(sql_course,[])
        #[{'course_number': 1}, {'course_number': 2}]
        # print(student_selected_course)
        stu=[]#所有已选课程的编号
        for item in student_selected_course:
            stu.append(item['course_number'])
        print(stu)

        course=[]#找出所有课程的编号
        for item in all_course:
            course.append(item['course_number'])

        print(course)
        ans=list(set(course)-set(stu))#未选课程

        print(ans)

#以下为检索未选中的课程
        not_selected_course_list=[]
        sql_not_selected = """
                    SELECT
        	course.course_name,
        	course.time,
        	teacher.`name`,
        	course.credit 
        FROM
        	course,
        	teacher 
        WHERE
        	course.course_number = %s 
        	AND course.teacher_name = teacher.id
                    """
        for item in ans:
            not_selected_course=obj.getone(sql_not_selected,[item,])
            not_selected_course['course_number']=item
            not_selected_course_list.append(not_selected_course)
        print(not_selected_course_list)



        return render(request,'SelectCourse.html',{'course_list':course_list,'not_selected_course_list':not_selected_course_list,'msg':user})
    else:pass


def add_my_course(request):
    global course_number
    sql="""
    
    INSERT INTO `course_student`(`course_number`, `student`) VALUES (%s, %s)
    
    """

    if request.method=='POST':
        obj = sqlhelper.SqlHelper()
        obj.create(sql,[course_number,username])

        print('==========================',course_number)
        return redirect('/select_course/')

    else:

        course_number=request.GET.get('nid')
        # print(course_number)
        return  render(request,'add_my_course.html',{'course_number':course_number})

def del_my_course(request):
    global del_course_number
    sql="""
    DELETE FROM `dangdang`.`course_student` WHERE `course_number` = %s AND `student` = %s LIMIT 1
    """
    if request.method=="GET":
        del_course_number=request.GET.get('cid')
        return render(request,'del_my_course.html',{'del_course_number':del_course_number})
    else:
        obj=sqlhelper.SqlHelper()
        obj.modify(sql,[del_course_number,username])
        return redirect('/select_course/')

def login(request):
    global g_username

    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        global username
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_user=request.POST.get('type')#检查登录的人的身份
        print('=====================',login_user)
        g_username=username
        try:
            if login_user=='admin':

                if sqlhelper.SqlHelper().getone('select password from admin where `name`=%s', [username, ])['password']==password:
                    obj = redirect('/layout/')
                obj.set_signed_cookie('ticket', '666', salt='qst')  # 设置签名，加盐
                """
                max_age: 存在10s，expire:具体的时间如2019/7/22/22:20:35
                path:cookie的写入地址
                """
                return obj
            elif  sqlhelper.SqlHelper().getone('select password from student where id=%s', [username, ])['password']!=password:
                return redirect('/login/')
            elif sqlhelper.SqlHelper().getone('select password from student where id=%s', [username, ])['password'] == password:
                obj=redirect('/select_course/')
                obj.set_signed_cookie('ticket', 'passport', salt='qst')
                return obj
        except Exception as e:
            print(e)
            return redirect('/login/')
