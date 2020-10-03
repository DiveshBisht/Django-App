from django.shortcuts import render
from django.urls import reverse
from django .shortcuts import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import datetime
import myapp.file_reader
from .models import testDetail, studentProfile, testQuestion, studentMark, clientProfile
from .forms import clientRegForm, clientLoginForm, studentRegForm, studenLoginForm, saveTestDetails, saveMarks, testIdVal


def index(request):
	try:
		return render(request, 'myapp/index.html')
	except:
		return HttpResponse("Something went wrong")


def about(request):
	try:
		return render(request, 'myapp/about.html')
	except:
		return HttpResponse("Something went wrong")


def trytest(request):
	cemail = clientProfile.objects.get(email="admin@admin.com")
	tests = testDetail.objects.filter(client_id= cemail.id)
	return render(request, 'myapp/trytest.html', {'tests': tests})






def studentlogin(request):
	try:
		return render(request, 'myapp/studentlogin.html')
	except:
		return HttpResponse("Something went wrong")


def studentregister(request):
	try:
		if request.method == 'POST':
			test_id = request.POST.get('test_id')
			try:
				testfile_id = testDetail.objects.get(test_id=test_id)
				request.session['test_id'] = test_id
			except testDetail.DoesNotExist:
				return HttpResponse("Invalid test ID")
			return render(request, 'myapp/studenthome.html', {'testid': testfile_id})
	except:
		return HttpResponse("Something went wrong")


def studentloginVal(request):
	try:
		if request.method == 'POST':
			log = studenLoginForm(request.POST)
			if log.is_valid():
				try:
					user = studentProfile.objects.get(email=log.cleaned_data.get('email').strip(),
													  password=log.cleaned_data.get('password').strip())
					request.session['studentuid'] = user.id
					test_id = request.session.get('test_id')
					return HttpResponseRedirect(reverse('taketest'))
				except studentProfile.DoesNotExist:
					return HttpResponse("Invalid username or password")
	except:
		return HttpResponse("Something went wrong")


def studentregisterVal(request):
	try:
		if request.method == 'POST':
			addstudent = studentRegForm(request.POST)
			if addstudent.is_valid():
				emailcheck = studentProfile.objects.filter(
					email=addstudent.cleaned_data.get('email').strip())
				if(emailcheck.count() > 0):
					return HttpResponse("This email is already registered")
				else:
					p = studentProfile(
						name=addstudent.cleaned_data.get('name').strip(),
						email=addstudent.cleaned_data.get('email').strip(),
						rollno=addstudent.cleaned_data.get('rollno').strip(),
						password=addstudent.cleaned_data.get(
							'password').strip(),
						client=addstudent.cleaned_data.get('client').strip(),
					)
					p.save()
					request.session['studentuid'] = p.id
		return HttpResponseRedirect(reverse('taketest'))
	except:
		return HttpResponse("Something went wrong")


def studentlogout(request):
	try:
		del request.session['studentuid']
		del request.session['test_id']
		return HttpResponseRedirect(reverse('index'))
	except:
		pass
	return HttpResponseRedirect(reverse('index'))






def taketest(request):
	try:
		if request.session.has_key('studentuid') and request.session.has_key('test_id'):
			studentid = request.session['studentuid']
			testid = request.session['test_id']
			try:
				user = studentProfile.objects.get(pk=studentid)
				ques = testQuestion.objects.filter(question_id=testid)
				noOfQuestions = ques.count()
				time = testDetail.objects.get(test_id=testid)
				return render(request, 'myapp/taketest.html', {'user_id': user, 'ques': ques, 'timer': time, 'noOfQuestions': noOfQuestions})
			except Exception as e:
				return HttpResponse("Something went wrong")
		else:
			return HttpResponseRedirect(reverse('studentlogin'))
	except:
		return HttpResponse("Something went wrong")


def papersubmit(request):
	try:
		if request.method == 'POST':
			addmarks = saveMarks(request.POST)
			test_id = request.session['test_id']
			student_id = request.session['studentuid']
			obj = testDetail.objects.get(test_id=test_id)
			obj1 = studentProfile.objects.get(pk=student_id)
			if addmarks.is_valid():
				p = studentMark(
					ques_paper_id=test_id,
					studentid=student_id,
					client=obj.client_id,
					testtitle=obj.testtitle,
					email=obj1.email,
					name=obj1.name,
					marks=addmarks.cleaned_data.get('totalmarks'),
				)
				p.save()
		return HttpResponseRedirect(reverse('studentlogout'))
	except:
		return HttpResponse("Something went wrong")





def clientregister(request):
	try:
		return render(request, 'myapp/clientregister.html')
	except:
		return HttpResponse("Something went wrong")


def clientlogin(request):
	try:
		return render(request, 'myapp/clientlogin.html')
	except:
		return HttpResponse("Something went wrong")


def clientregisterVal(request):
	try:
		if request.method == 'POST':
			signup = clientRegForm(request.POST)
			if signup.is_valid():
				try:
					c = clientProfile(
						name=signup.cleaned_data.get('name').strip(),
						email=signup.cleaned_data.get('email').strip(),
						contactNumber=signup.cleaned_data.get(
							'contactNumber').strip(),
						pwd=signup.cleaned_data.get('pwd').strip(),
					)
					c.save()
					request.session['user_id'] = c.id
				except clientProfile.DoesNotExist:
					return HttpResponse("Email already registered")
		return HttpResponseRedirect(reverse('clienthome'))
	except:
		return HttpResponse("Something went wrong")


def clientloginVal(request):
	try:
		if request.method == 'POST':
			log = clientLoginForm(request.POST)
			if log.is_valid():
				try:
					user = clientProfile.objects.get(email=log.cleaned_data.get(
						'email').strip(), pwd=log.cleaned_data.get('pwd').strip())
					request.session['user_id'] = user.id
					
					return HttpResponseRedirect(reverse('clienthome'))
				except clientProfile.DoesNotExist:
					return HttpResponse("Wrong username or password")
	except:
		return HttpResponse("Something went wrong")


def clienthome(request):
	try:
		if request.session.has_key('user_id'):
			uid = request.session['user_id']
			try:
				clientobj = clientProfile.objects.get(pk=uid)
				testinfo_list = testDetail.objects.filter(client_id=uid)
				paginator = Paginator(testinfo_list, 3) # Show 3 tests per page

				page = request.GET.get('page')
				try:
					testinfo = paginator.page(page)
				except PageNotAnInteger:
				# If page is not an integer, deliver first page.
					testinfo = paginator.page(1)
				except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
					testinfo = paginator.page(paginator.num_pages)
				return render(request, 'myapp/clienthome.html', {'client_id': clientobj, 'test': testinfo})
			except clientProfile.DoesNotExist:
				return HttpResponse("User not found")
		else:
			return render(request, 'myapp/index.html')
	except:
		return HttpResponse("Something went wrong")

def clientlogout(request):
	try:
		del request.session['user_id']
		return HttpResponseRedirect(reverse('index'))
	except:
		pass
	return HttpResponseRedirect(reverse('index'))






def addtest(request):
	try:
		uid = request.session['user_id']
		client = clientProfile.objects.get(pk=uid)
		return render(request, 'myapp/addtest.html', {'client_id': client})
	except:
		return HttpResponse("Something went wrong")


def upload(request):
	try:
		form = saveTestDetails(request.POST or None, request.FILES or None)
		if request.method == 'POST' and request.FILES['myfile'] and form.is_valid():
			now = str(datetime.now().strftime("%Y%m%d%H%M%S"))
			print(now)
			now = now + str(request.session['user_id'])
			myfile = request.FILES['myfile']
			ext = myfile.name[myfile.name.rfind('.'):]
			fs = FileSystemStorage()
			filename = fs.save(now + ext, myfile)
			myapp.file_reader.file_to_db(
				filename, str(request.session['user_id']), now)
			
			p = testDetail(
				test_id=now,
				client_id=str(request.session['user_id']).strip(),
				testtitle=form.cleaned_data.get('testtitle').strip(),
				testduration=form.cleaned_data.get('testduration').strip(),
			)
			p.save()
			return render(request, 'myapp/addtest.html', {'uploaded_file_url': now})
		return render(request, 'myapp/addtest.html', {'client_id': client})
	except:
		return HttpResponse("Something went wrong")


def deletetest(request, test_id):
	try:
		test = testDetail.objects.get(pk=test_id)
		questions = testQuestion.objects.filter(question_id=test.test_id)
		deleteMarks = studentMark.objects.filter(ques_paper_id=test.test_id)
		test.delete()
		for i in questions:
			questions.delete()
		for j in deleteMarks:
			deleteMarks.delete()
		return HttpResponseRedirect(reverse('clienthome'))
	except:
		return HttpResponse("Cannot Delete Test")


def studentinfo(request):
	try:
		uid = request.session['user_id']
		client1 = clientProfile.objects.get(pk=uid)
		stuInfo = studentProfile.objects.filter(client=uid)
		return render(request, 'myapp/studentinfo.html', {'client_id': client1, 'stuInfo': stuInfo})
	except:
		return HttpResponse("Something went wrong")


def studentmarks(request):
	try:
		uid = request.session['user_id']
		client1 = clientProfile.objects.get(pk=uid)
		stuMarks = studentMark.objects.filter(client=uid)
		return render(request, 'myapp/studentmarks.html', {'client_id': client1, 'stuMarks': stuMarks})
	except:
		return HttpResponse("Something went wrong")

		
		