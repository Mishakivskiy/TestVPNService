import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse
from django.db.models import Sum
from bs4 import BeautifulSoup as BS
from .forms import EditProfileForm, UserSiteForm
from .models import UserSite, SiteStats


def home(request):
    return render(request, 'product/home.html', {'user': request.user})


@login_required
def profile(request):
    user_sites = UserSite.get_user_sites(request.user)
    form = UserSiteForm()

    site_stats = SiteStats.objects.filter(site__in=user_sites).values('site_id').annotate(total_clicks=Sum('clicks'),
                                                                                          total_traffic=Sum('traffic'))
    for stats in site_stats:
        stats['total_traffic_mb'] = stats['total_traffic'] / (1024 * 1024)
        stats['site'] = UserSite.objects.get(id=stats['site_id']).name

    print(site_stats)

    return render(request, 'product/profile.html', {'user': request.user, 'user_sites': user_sites, 'form': form, 'site_stats': site_stats})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'product/edit_profile.html', {'form': form})


@login_required
def add_site(request):
    if request.method == 'POST':
        form = UserSiteForm(request.POST)
        if form.is_valid():
            user_site = form.save(commit=False)
            user_site.user = request.user
            user_site.save()
            return redirect('profile')

    return redirect('profile')


def test(request):
    site = requests.get('https://www.pcarmarket.com/')
    content = site.text
    return HttpResponse(content)


@login_required
def proxy_site(request, user_site_name, site_url):
    user_site = get_object_or_404(UserSite, user=request.user, name=user_site_name)
    user_site.add_click()

    parsed_user_site_url = urlparse(site_url)
    response = requests.get(site_url)
    user_site.add_traffic(request, response)

    soup = BS(response.content, "html.parser")
    def update_attr(tag, attr_name):
        parsed_attr = urlparse(tag[attr_name])
        original_parsed = (parsed_user_site_url.scheme, parsed_user_site_url.netloc)

        if (parsed_attr.scheme, parsed_attr.netloc) == original_parsed:
            tag[attr_name] = f'/{user_site_name}/{tag[attr_name]}'
        elif not parsed_attr.scheme and not parsed_attr.netloc:
            tag[attr_name] = (
                f'/{user_site_name}/{parsed_user_site_url.scheme}://{parsed_user_site_url.netloc}'
                f'{tag[attr_name]}'
            )

    def get_tags(tag_names, attribute):
        return [tag for tag_name in tag_names for tag in soup.find_all(tag_name, **{attribute: True})]

    tags_with_href = ["a", "link", "img", "script", "audio", "video", "source"]
    tags_with_src = ["img", "script", "audio", "video", "source"]

    for tag in get_tags(tags_with_href, "href"):
        update_attr(tag, "href")

    for tag in get_tags(tags_with_src, "src"):
        update_attr(tag, "src")

    return HttpResponse(str(soup))
