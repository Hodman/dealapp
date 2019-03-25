from django.views.generic import View
from django.shortcuts import render, redirect, reverse

from .models import Goods, GoodsFeedback
from .forms import GoodsFeedbackForm

from itertools import chain
# Create your views here.


class AllGoodsView(View):
    template = 'goods/all_goods.html'

    def get(self, request):
        all_goods = Goods.objects.all()
        return render(request, self.template, locals())


class ProductDetailView(View):
    template_name = 'goods/product_detail.html'
    feedbacks = []

    # def get(self, request, product_id):
    #     form = GoodsFeedbackForm()
    #     feedbacks = []
    #     try:
    #         product = Goods.objects.get(id=product_id)
    #         feedback = GoodsFeedback.objects.filter(product=product, comment=None)
    #         for feed in feedback:
    #             self.feedbacks.append(feed)
    #             self.feedloop(feed)
    #             feedbacks += self.feedbacks
    #             self.feedbacks.clear()
    #     except GoodsFeedback.DoesNotExist:
    #         feedback = None
    #     return render(request, self.template_name, locals())
    # #
    # # def feedloop(self, feed):
    # #     variable = 'comment'
    # #     feedback_replay = GoodsFeedback.objects.filter(**{variable: feed})
    # #     if feedback_replay:
    # #         variable += '__comment'
    # #         self.feedloop(feedback_replay)
    #
    # def feed_appender(self, feedback):
    #     for feed in feedback:
    #         self.feedbacks.append(feed)
    #         self.feedloop(feed)
    #
    # #     return self.feedbacks
    # def feedloop(self, feed):
    #     feedback_replay = GoodsFeedback.objects.filter(comment=feed)
    #     if feedback_replay:
    #         self.feed_appender(feedback_replay)

    def get(self, request, product_id):
        form = GoodsFeedbackForm()
        feedbacks = []
        try:
            product = Goods.objects.get(id=product_id)
            feedback = GoodsFeedback.objects.filter(product=product, comment=None)
            for feed in feedback:
                feedbacks.append(feed)
                branch = GoodsFeedback.objects.filter(product=product, branch=feed.branch)
                feedbacks.append(branch)
                print(feedbacks)
        except GoodsFeedback.DoesNotExist:
            print(123)
        return render(request, self.template_name, locals())

    def post(self, request, product_id, **kwargs):
        form = GoodsFeedbackForm(data=request.POST)
        print(request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.product_id = product_id
            feedback.writer = request.user
            try:
                replay = GoodsFeedback.objects.get(id=request.POST['replay-comment-id'])
                feedback.comment = replay
            except ValueError:
                feedback.comment = None
            feedback.save()
        return redirect(reverse('all_goods:product_view', kwargs={'product_id': product_id}))

