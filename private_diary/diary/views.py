import logging

from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import InquiryForm
from .models import Diary

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy("diary:inquiry")

    def form_valid(self, form: InquiryForm):
        form.send_email()
        messages.success(self.request, "メッセージを送信しました。")
        logger.info("Inquiry sent by {}".format(form.cleaned_data["name"]))
        return super().form_valid(form)


class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = "diary_list.html"

    def get_queryset(self):
        diaries = Diary.objects.filter(user=self.request.user).order_by("-created_at")
        return diaries
