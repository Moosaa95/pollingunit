from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .models import PollingUnit, ElectionResult,  LGA, Ward
from django.views.generic import ListView

class PollingUnitResultsView(View):
    template_name = 'polling/polling_unit_results.html'

    def get(self, request, polling_unit_id):
        polling_unit = get_object_or_404(PollingUnit, id=polling_unit_id)
        results = ElectionResult.objects.filter(polling_unit=polling_unit)
        return render(request, self.template_name, {'polling_unit': polling_unit, 'results': results})


class PollingUnitSearchView(View):
    template_name = 'polling/polling_unit_search.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        polling_unit_id = request.POST.get('polling_unit_id')
        print(polling_unit_id)
        if polling_unit_id:
            polling_unit = get_object_or_404(PollingUnit, id=polling_unit_id)
            results = ElectionResult.objects.filter(polling_unit=polling_unit)
            return render(request, 'polling/polling_unit_results.html', {'polling_unit': polling_unit, 'results': results})
        else:
            return render(request, self.template_name, {'error_message': 'Please enter a valid Polling Unit ID.'})




class LGASummedResultsView(View):
    template_name = 'polling/lga_summed_results.html'

    def get(self, request):
        lgas = LGA.objects.all()
        return render(request, self.template_name, {'lgas': lgas})

    def post(self, request):
        lga_id = request.POST.get('lga_id')
        if lga_id:
            selected_lga = get_object_or_404(LGA, id=lga_id)
            results = ElectionResult.objects.filter(polling_unit__ward__lga=selected_lga)
            
            summed_results = {}
            for result in results:
                if result.party in summed_results:
                    summed_results[result.party] += result.score
                else:
                    summed_results[result.party] = result.score

            return render(request, self.template_name, {'selected_lga': selected_lga, 'summed_results': summed_results})
        else:
            lgas = LGA.objects.all()
            return render(request, self.template_name, {'lgas': lgas, 'error_message': 'Please select a Local Government.'})

class WardDetailView(View):
    template_name = 'polling/ward_detail.html'

    def get(self, request, ward_id):
        ward = get_object_or_404(Ward, id=ward_id)
        return render(request, self.template_name, {'ward': ward})
    
# class EnterPollingUnitResultsView(View):
#     template_name = 'polling/enter_polling_unit_results.html'

#     def get(self, request):
#         lgas = LGA.objects.all()
#         return render(request, self.template_name, {'lgas': lgas})

#     def post(self, request):
#         lga_id = request.POST.get('lga_id')
#         ward_id = request.POST.get('ward_id')

#         if lga_id and ward_id:
#             selected_lga = get_object_or_404(LGA, id=lga_id)
#             print(selected_lga, 'please')
#             selected_ward = get_object_or_404(Ward, id=ward_id)

#             return render(request, self.template_name, {'lgas': lgas, 'selected_lga': selected_lga, 'selected_ward': selected_ward})
#         else:
#             lgas = LGA.objects.all()
#             return render(request, self.template_name, {'lgas': lgas, 'error_message': 'Please select a Local Government and Ward.'})

# class EnterPollingUnitResultsView(View):
#     template_name = 'polling/enter_polling_unit_results.html'

#     def get(self, request):
#         lgas = LGA.objects.all()
#         parties = Party.objects.all()
#         return render(request, self.template_name, {'lgas': lgas, 'parties': parties})

#     def post(self, request):
#         lga_id = request.POST.get('lga_id')
#         ward_id = request.POST.get('ward_id')
#         polling_unit_name = request.POST.get('polling_unit_name')

#         if lga_id and ward_id and polling_unit_name:
#             selected_lga = get_object_or_404(LGA, id=lga_id)
#             selected_ward = get_object_or_404(Ward, id=ward_id)

#             polling_unit = PollingUnit(name=polling_unit_name, ward=selected_ward)
#             polling_unit.save()

#             parties = Party.objects.all()
#             for party in parties:
#                 score_field_name = f'party_{party.id}'
#                 score = int(request.POST.get(score_field_name, 0))

#                 result = ElectionResult(polling_unit=polling_unit, party=party, score=score)
#                 result.save()

#             return redirect('success_page')  # Redirect to a success page
#         else:
#             lgas = LGA.objects.all()
#             parties = Party.objects.all()
#             return render(request, self.template_name, {'lgas': lgas, 'parties': parties, 'error_message': 'Please fill in all required fields.'})
class EnterPollingUnitResultsView(View):
    template_name = 'polling/enter_polling_unit_results.html'

    def get(self, request):
        lgas = LGA.objects.all()
        return render(request, self.template_name, {'lgas': lgas})

    def post(self, request):
        lga_id = request.POST.get('lga_id')
        ward_id = request.POST.get('ward_id')
        polling_unit_name = request.POST.get('polling_unit_name')

        print('poster')
        if lga_id and ward_id and polling_unit_name:
            selected_lga = get_object_or_404(LGA, id=lga_id)
            selected_ward = get_object_or_404(Ward, id=ward_id)
            # ward_save = Ward()

            polling_unit = PollingUnit(name=polling_unit_name, ward=selected_ward)
            polling_unit.save()

            party = request.POST.get('party_name')
            score = int(request.POST.get('scores', 0))

            print(party, score)
            results = {}

           
            result = ElectionResult(polling_unit=polling_unit, party=party, score=score)
            result.save()

            return render(request, 'polling/polling_unit_results.html', {'polling_unit': polling_unit, 'results': results})
        else:
            lgas = LGA.objects.all()
            return render(request, self.template_name, {'lgas': lgas, 'error_message': 'Please fill in all required fields.'})

class GetWardsView(View):
    def get(self, request):
        lga_id = request.GET.get('lga_id')
        wards = []

        if lga_id:
            wards = Ward.objects.filter(lga_id=lga_id)

        ward_options = [{'id': ward.id, 'name': ward.name} for ward in wards]
        return JsonResponse({'wards': ward_options})


class WardListView(ListView):
    model = Ward
    template_name = 'polling/ward_list.html'
    context_object_name = 'wards'