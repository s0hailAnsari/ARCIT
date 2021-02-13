from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from Doctor.forms import DoctorForm, DoctorUserForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from DiagnosticDepartment.models import DiagnosticDepartmentReport

from .models import Doctor
from Patient.models import Patients, PatientHistory
from Patient.forms import PatientHistoryForm

# def index(request):
#     if request.method == 'POST':
    
User = get_user_model()
class DoctorView(TemplateView):
    template_name='Doctor/registeration.html'
    
    def get(self,request):
        form = DoctorForm()
        form2 = DoctorUserForm()
        return render(request,self.template_name,{'form':form, 'form2': form2})
     
    def post(self,request):
        if request.method == 'POST':
            form =  DoctorUserForm(request.POST)
            form2 = DoctorForm(request.POST)
            if form.is_valid() and form2.is_valid():              

                User = get_user_model()

                user = User.objects.create_user(
                    form.data['username'], 
                    form2.data['email'], 
                    form.data['password1'], 
                    first_name=form2.data['first_name'],
                    last_name=form2.data['last_name'],
                    is_doctor = True,
                )
                patform=form2.save(commit=False) 
                patform.user=user
                patform.save()

                # user = authenticate(username=form2.data['username'], password=form2.data['password1'])
                # login(request, user)
                return redirect('login')
            else:
                form = DoctorUserForm()
                form2=DoctorForm()
            return render(request,self.template_name, {'form': form,'form2':form2})
            
class ViewDocotrProfile(TemplateView):
    template_name='Doctor/profile.html'

    def get(self,request):        
        user = User.objects.get(username=request.session['loggedin_username'])
        print(user)
        doctor = Doctor.objects.get(user=user)
        # today = date.today()
        # age = today.year - datetime.year(patient.dob) - ((today.month, today.day) < (datetime.month(patient.dob), datetime.day(patient.dob)))
        # age = patient.dob
        return render(request,self.template_name,{'profile':doctor})

class ViewPatientReports(TemplateView):
    template_name='Doctor/viewPatientReport.html'

    def get(self,request):
        user = Patients.objects.get(phone_number=request.session['phoneNumber']).user
        model = DiagnosticDepartmentReport.objects.filter(user=user)

        return render(request,self.template_name,{'models':model})


class AddPatientDataView(TemplateView):
    template_name='Doctor/addPatientHistory.html'

    def get(self,request):
        form = PatientHistoryForm()

        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=PatientHistoryForm(request.POST)
        if request.method == 'POST':

            user = Patients.objects.get(phone_number=request.session['phoneNumber']).user
            doctor_user = User.objects.get(username=request.session['loggedin_username'])

            if form.is_valid():
                formdata = form.save(commit=False)
                formdata.user=user
                formdata.referred_from = doctor_user
                formdata.save()

                # return render(request, 'Doctor/index.html')
                return redirect('viewpatienthistory')
        else:
            form = PatientHistoryForm()
            return render(request,self.template_name, {'form': form})

class ViewPatientHistory(TemplateView):
    template_name='Doctor/viewPatientHistory.html'

    def get(self,request):
        user = Patients.objects.get(phone_number=request.session['phoneNumber']).user
        model = PatientHistory.objects.filter(user=user)

        return render(request,self.template_name,{'models':model})
