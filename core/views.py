# myapp/views.py

# myapp/views.py
# myapp/views.py

from django.shortcuts import render, redirect
from django.db.models import Sum
from .forms import InputDataForm
from .models import InputData
import os
from django.http import HttpResponse
from django.utils.text import slugify

def home(request):
    if request.method == 'POST':
        form = InputDataForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            nation = instance.nation
            instance.nation_name = nation.name  # Save the full name of the country

            # Define nation groups using full names
            group_1_nations = ["United States of America", "Canada", "Mexico"]
            group_2_nations = ["Italy", "France", "Germany"]
            group_3_nations = ["Japan", "China", "South Korea"]

            if instance.nation_name in group_1_nations:
                instance.group = 'Group 1'
            elif instance.nation_name in group_2_nations:
                instance.group = 'Group 2'
            elif instance.nation_name in group_3_nations:
                instance.group = 'Group 3'
            else:
                instance.group = 'Group Unknown'

            instance.save()
            return redirect('home')
    else:
        form = InputDataForm()

    # Aggregate data by group and sum numbers by nation
    group_1_data = InputData.objects.filter(group='Group 1').values('nation_name').annotate(total=Sum('number')).order_by('nation_name')
    group_2_data = InputData.objects.filter(group='Group 2').values('nation_name').annotate(total=Sum('number')).order_by('nation_name')
    group_3_data = InputData.objects.filter(group='Group 3').values('nation_name').annotate(total=Sum('number')).order_by('nation_name')

    # Calculate the total sum for each group
    group_1_total = InputData.objects.filter(group='Group 1').aggregate(total=Sum('number'))['total'] or 0
    group_2_total = InputData.objects.filter(group='Group 2').aggregate(total=Sum('number'))['total'] or 0
    group_3_total = InputData.objects.filter(group='Group 3').aggregate(total=Sum('number'))['total'] or 0

    context = {
        'form': form,
        'group_1_data': group_1_data,
        'group_2_data': group_2_data,
        'group_3_data': group_3_data,
        'group_1_total': group_1_total,
        'group_2_total': group_2_total,
        'group_3_total': group_3_total,
    }

    return render(request, 'core/homepage.html', context)




def delete_all_data(request):
    InputData.objects.all().delete()
    return redirect('home')  # Reindirizza alla homepage dopo la cancellazione


def export_data(request):
    # Raggruppa i dati per zona
    group_1_data = InputData.objects.filter(group='Group 1')
    group_2_data = InputData.objects.filter(group='Group 2')
    group_3_data = InputData.objects.filter(group='Group 3')

    lines = []

    # Zona 1
    lines.append("Zona 1:\n")
    for item in group_1_data:
        lines.append(f"{item.nation_name}: {item.number}\n")

    # Aggiungi una linea vuota per separare le zone
    lines.append("\n")

    # Zona 2
    lines.append("Zona 2:\n")
    for item in group_2_data:
        lines.append(f"{item.nation_name}: {item.number}\n")

    # Aggiungi una linea vuota per separare le zone
    lines.append("\n")

    # Zona 3
    lines.append("Zona 3:\n")
    for item in group_3_data:
        lines.append(f"{item.nation_name}: {item.number}\n")

    # Unisci le linee in un unico contenuto
    content = ''.join(lines)

    # Prepara la risposta HTTP per il download del file
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="exported_data.txt"'

    return response
