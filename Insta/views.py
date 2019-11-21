from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from Insta.models import Post, Like
from Insta.forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

class HelloWorld(TemplateView):
	template_name = 'test.html'

class PostsView(ListView):
	model = Post
	template_name = 'index.html'

class PostDetailView(DetailView):
	model = Post
	template_name = 'post_detail.html'
		
class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = 'post_create.html'
	fields = '__all__' # 需要用户提供所有信息
	login_url = 'login'

class PostUpdateView(UpdateView):
	model = Post
	template_name = 'post_update.html'
	fields = ['title']

class PostDeleteView(DeleteView):
	model = Post
	template_name = 'post_delete.html'
	success_url = reverse_lazy("HelloWorld")

class SignUp(CreateView):
	form_class = CustomUserCreationForm # 基于什么样的form，什么model，什么field
	template_name = 'signup.html' # 使用什么样的HTML
	success_url = reverse_lazy("login") # 成功后跳转到哪里

@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }