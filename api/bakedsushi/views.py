from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .forms import ContactListForm
from .models import ContactListModel
from .serializers import ContactListSerializer
from rest_framework import generics, parsers, status
from django.template.loader import render_to_string
from django.core import mail
from django.utils.html import strip_tags
from django.core.mail import send_mail
import json  # Add this import
from django.core.mail import EmailMultiAlternatives
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from rest_framework import generics, parsers, status

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class ContactListView(APIView):
  def get(self, request, format=None):
    obj = ContactListModel.objects.all()
    serializer = ContactListSerializer(obj, many=True)
    
    return Response(serializer.data)

  def post(self, request):
    try:
      form = ContactListForm(request.data)

      if not form.is_valid():
        return Response({
          'status': 'error',
          'message': 'Invalid form data',
          'errors': form.errors
        }, status=status.HTTP_400_BAD_REQUEST)
      
      # Save the object to the database
      obj = form.save(commit=False)
      obj.save()

      # Build context after validation
      context = {
        "contact_id": form.cleaned_data.get('contact_id'),
        "firstname": form.cleaned_data.get('firstname'),
        "lastname": form.cleaned_data.get('lastname'),
        "contact_email": form.cleaned_data.get('contact_email'),
        "contact_number": form.cleaned_data.get('contact_number'),
        "message": form.cleaned_data.get('message'),
      }

      firstname = form.cleaned_data.get('firstname')
      lastname = form.cleaned_data.get('lastname')
      recipient_email = form.cleaned_data.get('contact_email')

      # Subject lines
      subject_inquiry = f"Inquiry from {firstname} {lastname}"
      subject_thankyou = "Thank You for Contacting Fabrics Plus"

      # Render HTML templates
      html_message_inquiry = render_to_string('contact.html', context)
      plain_message_inquiry = strip_tags(html_message_inquiry)

      html_message_thankyou = render_to_string('thankyou.html', context)
      plain_message_thankyou = strip_tags(html_message_thankyou)

      from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '') or getattr(settings, 'EMAIL_HOST_USER', '')
      email_backend = getattr(settings, 'EMAIL_BACKEND', '')

      if email_backend == 'django.core.mail.backends.smtp.EmailBackend' and not from_email:
        return Response({
          'status': 'created',
          'id': obj.id,
          'email_status': 'skipped',
          'message': 'Contact record created. Email credentials are not configured.'
        }, status=status.HTTP_201_CREATED)

      # Internal team recipients
      internal_recipients = list(filter(None, [
        getattr(settings, 'EMAIL_HOST_USER', ''),
        'info@techsavvies.space'
      ]))

      try:
        # Send inquiry email to team
        mail.send_mail(
          subject_inquiry,
          plain_message_inquiry,
          from_email,
          internal_recipients,
          html_message=html_message_inquiry,
          fail_silently=False
        )

        # Send thank-you email to inquirer
        mail.send_mail(
          subject_thankyou,
          plain_message_thankyou,
          f'BAKEDSUSHI <{from_email}>',
          [recipient_email],
          html_message=html_message_thankyou,
          fail_silently=False
        )

        return Response({
          'status': 'created',
          'id': obj.id,
          'email_status': 'sent'
        }, status=status.HTTP_201_CREATED)

      except Exception as email_error:
        print(f"Email sending error: {email_error}")
        traceback.print_exc()
        return Response({
          'status': 'created',
          'id': obj.id,
          'email_status': 'failed',
          'message': 'Contact record created, but email notifications failed.'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
      print(f"General error in ContactListView POST: {e}")
      traceback.print_exc()
      return Response({
        'status': 'error',
        'message': 'Internal server error'
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class ContactCreateView(APIView):
  def post(self, request):
    form = ContactListForm(request.data)

    if form.is_valid():
      obj = form.save(commit=False)
      obj.save()

      return Response({'status':'created'})
    else:
      return Response({'status':'errors', 'errors': form.errors})
  
  def put(self, request, pk):
    obj = ContactListModel.objects.get(pk=pk)
    form = ContactListForm(request.data, instance=obj)
    form.save()

    return Response({'status': 'updated'})

  def delete(self, request, pk):
    obj = ContactListModel.objects.get(pk=pk)
    obj.delete()

    return Response({'status': 'deleted'})
  
class ContactDetailView(APIView):
  def get(self, request, pk, format=None):
    obj = ContactListModel.objects.get(pk=pk)
    serializer = ContactListSerializer(obj)

    return Response(serializer.data)
  
