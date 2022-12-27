import logging

from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

from .forms import InquiryForm

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
