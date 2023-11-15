from django.db import models
from django.contrib.auth.models import User


class UserSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name

    @classmethod
    def get_user_sites(cls, user):
        return cls.objects.filter(user=user)

    def get_site_stats(self):
        site_stats, created = SiteStats.objects.get_or_create(site=self)
        return site_stats

    def add_click(self):
        site_stats = self.get_site_stats()
        site_stats.add_click()

    def add_traffic(self, request, response):
        site_stats = self.get_site_stats()
        site_stats.add_traffic(request, response)


class SiteStats(models.Model):
    site = models.ForeignKey(UserSite, on_delete=models.CASCADE)
    clicks = models.PositiveIntegerField(default=0)
    traffic = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.site.name}"

    def add_click(self):
        self.clicks += 1
        self.save()

    def add_traffic(self, request, response):
        request_header_size = len(str(request.META).encode("utf-8"))
        request_body_size = (len(response.request.body) if response.request.body else 0)
        sent_data_size = request_header_size + request_body_size

        response_header_size = len(str(response.headers).encode("utf-8"))
        response_body_size = len(response.content)
        received_data_size = response_header_size + response_body_size

        self.traffic += sent_data_size + received_data_size
        self.save()
