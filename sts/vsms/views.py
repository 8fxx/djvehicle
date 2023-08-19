from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View,TemplateView, DetailView,ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from vsms.models import Unit, Brand, status, vehicle, Unit, Type
from vsms.forms import NewVehicleForm, NewStatusForm, filterform
from django.urls import reverse_lazy
from vsms.filters import VehicleFilter

from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from itertools import chain
from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

# LOGIN OUT
def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Landing'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('Landing'))
            else:
                return HttpResponse("Account not Active")
        else:
            print('someone tried to login')
            print("username: {} and Password: {} ".format(username,password))
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request,'login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

#home
def landingpage(request):
    vehicles = vehicle.objects.all()
    if request.method == 'POST':
        searched = request.POST['searched']
        lookup = (Q(name__icontains=searched))| (Q(model__icontains=searched)) | (Q(capacity__icontains=searched)) | (Q(lastlocation__icontains=searched)) | (Q(laststatus__icontains=searched))  
        vehicles = vehicle.objects.filter(lookup)
    runningcount = vehicle.objects.filter(laststatus='Running')
    groundedcount = vehicle.objects.filter(laststatus='Grounded')
    # lookup = (Q())
    brandss = Brand.objects.all()
    units = Unit.objects.all()
    types = Type.objects.all()
    return render(request, 'landing.html',{'types':types,'vehicle_list':vehicles,'brandss':brandss,'units':units,'running':runningcount,'grounded':groundedcount})

@login_required
def indexview(request):
    vehicles = vehicle.objects.all()
    if request.method == 'POST':
        searched = request.POST['searched']
        lookup = (Q(name__icontains=searched))| (Q(model__icontains=searched)) | (Q(capacity__icontains=searched)) | (Q(lastlocation__icontains=searched)) | (Q(laststatus__icontains=searched))  
        vehicles = vehicle.objects.filter(lookup)
    runningcount = vehicle.objects.filter(laststatus='Running')
    groundedcount = vehicle.objects.filter(laststatus='Grounded')
    # lookup = (Q())
    brandss = Brand.objects.all()
    units = Unit.objects.all()
    types = Type.objects.all()
    return render(request, 'index.html',{'types':types,'vehicle_list':vehicles,'brandss':brandss,'units':units,'running':runningcount,'grounded':groundedcount})

# VEHICLE
def brandview(request,pk):
    brandlist = vehicle.objects.filter(brand=pk)
    runningcount = vehicle.objects.filter(brand=pk,laststatus='Running')
    groundedcount = vehicle.objects.filter(brand=pk,laststatus='Grounded')
    brandss = Brand.objects.all()
    units = Unit.objects.all()
    types = Type.objects.all()
    return render(request, 'index.html', {'types':types, 'vehicle_list':brandlist,'brandss':brandss,'units':units,'running':runningcount,'grounded':groundedcount})

def unitview(request,unit):
    unitlist = vehicle.objects.filter(issuedtounit=unit)
    runningcount = vehicle.objects.filter(issuedtounit=unit,laststatus='Running')
    groundedcount = vehicle.objects.filter(issuedtounit=unit,laststatus='Grounded')
    brandss = Brand.objects.all()
    units = Unit.objects.all()
    types = Type.objects.all()
    return render(request, 'index.html', {'types':types,'vehicle_list':unitlist,'brandss':brandss,'units':units,'running':runningcount,'grounded':groundedcount})

def typeview(request,type):
    typelist = vehicle.objects.filter(type=type)
    runningcount = vehicle.objects.filter(type=type,laststatus='Running')
    groundedcount = vehicle.objects.filter(type=type,laststatus='Grounded')
    brandss = Brand.objects.all()
    units = Unit.objects.all()
    types = Type.objects.all()
    return render(request, 'index.html', {'types':types,'vehicle_list':typelist,'brandss':brandss,'units':units,'running':runningcount,'grounded':groundedcount})

class vehicledetail(DetailView):
    model = vehicle
    template_name = 'detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super(vehicledetail, self).get_context_data(*args, **kwargs)
        brandss = Brand.objects.all()
        units = Unit.objects.all()
        types = Type.objects.all()
        context.update({'brandss': brandss,'units':units,'types':types})
        return context

class createvehicle(CreateView):
    form_class = NewVehicleForm
    template_name = 'vehicleform.html'
    model = vehicle
    success_message = 'Your submission is sucessful!'
    def form_valid(self,form):
        form.instance.createdby = self.request.user
        return super().form_valid(form)
    def get_success_message(self):
            return self.success_message

def createvehicles(request):
    runningcount = vehicle.objects.filter(laststatus='Running')
    groundedcount = vehicle.objects.filter(laststatus='Grounded')
    lookup = (Q())
    brandss = Brand.objects.all()
    units = Unit.objects.all()
    types = Type.objects.all()
    template_name = 'vehicleform.html'
    form_class = NewVehicleForm
    form = form_class
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.instance.createdby = request.user
            form.save()
        return HttpResponseRedirect(reverse('Index'))
    return render(request, template_name, {'form': form,'types':types, 'vehicle_list':brandss,'brandss':brandss,'units':units,'running':runningcount,'grounded':groundedcount})

class updatevehicle(UpdateView):
    form_class = NewVehicleForm
    template_name = 'vehicleform.html'
    model = vehicle

class deletevehicle(DeleteView):
    model = vehicle
    success_url = reverse_lazy('Index')
    template_name = 'vdeleteconfirm.html'
    

# STATUS
@login_required
def createstatus(request,pk):
    vehicle_obj = get_object_or_404(vehicle,pk=pk)
    brandss = Brand.objects.all()
    units = Unit.objects.all()
    types = Type.objects.all()
    if request.method == 'POST':
        form = NewStatusForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            member = vehicle.objects.get(pk=pk)
            member.issuedtounit = status.allotmentunit
            member.laststatus = status.update
            member.lastlocation = status.allotmentlocation
            member.save()
            status = form.save(commit=False)
            status.vehicle = vehicle_obj
            status.createdby = request.user
            status.save()
            return redirect('detail', pk=vehicle_obj.pk)
    else:
        form = NewStatusForm()
    return render(request,'statusform.html',{'form':form,'types':types, 'brandss':brandss,'units':units})

class AddStatus(LoginRequiredMixin,CreateView):
    model = vehicle
    form_class = NewStatusForm
    template_name = 'statusform.html'
    success_message = 'detail'
    def form_valid(self,form):
        member = vehicle.objects.get(id=self.kwargs['pk'])
        member.issuedtounit = form.instance.allotmentunit
        member.lastlocation = form.instance.allotmentlocation
        form.instance.createdby_id = self.request.user.id
        member.save()
        form.instance.user = self.request.user
        form.instance.member_id = self.kwargs['pk']
        return super().form_valid(form)


class Editstatus(UpdateView):
    model = status
    template_name = 'statusform.html'
    form_class = NewStatusForm
    success_url = ''
    def form_valid(self,form):
        latest = status.objects.filter(vehicle=form.instance.vehicle).latest('id')
        vehicles = vehicle.objects.get(id=form.instance.vehicle.id)
        if latest.id == form.instance.id:
            vehicles = vehicle.objects.get(id=form.instance.vehicle.id)
            vehicles.laststatus = form.instance.update
            vehicles.issuedtounit = form.instance.allotmentunit
            vehicles.lastlocation = form.instance.allotmentlocation
            vehicles.save()
        return super().form_valid(form)


class deletestatus(DeleteView):
    model = status
    success_url = reverse_lazy('Index')
    template_name = 'sdeleteconfirm.html'

def statusapproval(request, pk):
    sstatus = get_object_or_404(status,pk=pk)
    sstatus.approvestatus()
    return redirect('detail',pk=sstatus.vehicle.pk)

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        lookup = (Q(name__icontains=searched))| (Q(model__icontains=searched)) | (Q(capacity__icontains=searched))
        vehicles = vehicle.objects.filter(lookup)

        return render(request,'search.html',{'searched':searched,'members':vehicles})
    else:
        return render(request,'search.html',{})

def charts(request):
    brandss = Brand.objects.all()
    units = Unit.objects.all()
    types = Type.objects.all()
    #total vehicles in unit
    unitss = Unit.objects.all()
    vehicless = vehicle.objects.all()
    unitslist = []
    vehiclelist = []
    labellist = []
    ylist = []
    data_points=[]
    for i in unitss:
        unitslist.append(str(i))
    for i in vehicless:
        vehiclelist.append(str(i.issuedtounit))
        
    for i in unitslist:
        ylist.append(vehiclelist.count(i))
        labellist.append(i)

    for i,j in zip(ylist,labellist):
        data_points.append({'label':j,'y':i})

    #running, ground
    runningdict = []
    runingcount = []
    grounddict = []
    groundcount = []
    runlabel = []
    groundlabel = []
    data_points_running=[]
    data_points_grounded = []
    for j in unitslist:
        for i in vehicless:
            if str(i.issuedtounit) == j and i.laststatus == 'Running':
                runningdict.append(str(i.issuedtounit))
    for j in unitslist:
        for i in vehicless:
            if str(i.issuedtounit) == j and i.laststatus == 'Grounded':
                grounddict.append(str(i.issuedtounit))
    for i in unitslist:
        runingcount.append(runningdict.count(i))
        runlabel.append(i)
    for i,j in zip(runingcount,runlabel):
        data_points_running.append({'label':j,'y':i})
    for i in unitslist:
        groundcount.append(grounddict.count(i))
        groundlabel.append(i)
    for i,j in zip(groundcount,groundlabel):
        data_points_grounded.append({'label':j,'y':i})
    print(data_points_running)
    print(data_points_grounded)
    return render(request, 'charts.html', {'types':types, 'brandss':brandss,'units':units, "data_points" : data_points,'unitss':unitss,'vehicless':vehicless,"data_points_running" : data_points_running,'data_points_grounded': data_points_grounded })      