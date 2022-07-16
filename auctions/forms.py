from socket import fromshare
from django import forms
from django.forms import ModelForm
from .models import Auction, Comment, Bid

category_choices = [('None' , 'None'),('Fashion' , 'Fashion'),('Entertainment', 'Entertainment'),('Homeware', 'Homeware'),('Art', 'Art'),('Fitness','Fitness'),('Other','Other')]

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'start_bid', 'content', 'category', 'image']
        widgets = {
            'category' : forms.Select(choices = category_choices, attrs={'class':'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

    # def __init__(self, *args, **kwargs):
    #     super(BidForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control m-2'
        