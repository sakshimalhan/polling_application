from django.shortcuts import render
from django.http import HttpResponseRedirect
from main import models,forms
from django.contrib.auth.decorators import login_required

from django.views.generic import (
    ListView,
    DetailView,
    FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.detail import SingleObjectMixin
class Index(ListView):
    model=models.Question
    template_name="main/ques_list.html"
class Question(SingleObjectMixin,FormView):

    model=models.Question
    template_name='main/question.html'
    form_class=forms.AnswerForm
    

    def get_context_data(self,**kwargs):
        data=super().get_context_data(**kwargs)
        data["answer"]=models.Answer.objects.filter(
            question=self.get_object(),
            user=self.request.user
        )
        if data["answer"]:
            data["answer"]=models.Answer.objects.get(
            question=self.get_object(),
            user=self.request.user
        )

        return data

    def form_valid(self,form):
        obj=form.save(commit=False)
        obj.question=self.get_object()
        obj.user=self.request.user
        obj.save()
        return HttpResponseRedirect('/')
    def post(self,request,*args,**kwargs) :
        self.object=self.get_object()  
        return super().post(request,*args,**kwargs)  
    def get(self,request,*args,**kwargs) :
        self.object=self.get_object()  
        context=self.get_context_data(object=self.object)
        return self.render_to_response(context)

# Create your views here.
