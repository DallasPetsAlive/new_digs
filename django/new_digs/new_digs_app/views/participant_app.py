from django.shortcuts import render


def participant_app(request):
    return render(request, 'new_digs_app/participant_app.html', {})
