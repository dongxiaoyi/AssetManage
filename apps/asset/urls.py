# _*_encoding:utf-8_*_
from django.conf.urls import url, include
from django.views.generic import TemplateView
from views import asset_report,asset_with_no_asset_id,NewAssetApprovalView,AssetListView,GetAssetListView,AssetCategoryView,AssetEventLogsView,AssetDetailView,GetDashboardDataView

urlpatterns = [
    #url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'report/$',  asset_report, name='report'),
    url(r'report/asset_with_no_asset_id/$', asset_with_no_asset_id, name='acquire_asset_id'),
    url(r'^new_assets_approval/$', NewAssetApprovalView, name="new_assets_approval"),
    url(r'^asset_list/$', AssetListView.as_view(), name="asset_list"),
    url(r'^asset_list/(\d+)/$', AssetDetailView.as_view(), name="asset_detail"),
    url(r'^asset_list/list/$', GetAssetListView.as_view(), name="get_asset_list"),
    url(r'^asset_list/category/$', AssetCategoryView.as_view(), name="asset_category"),
    url(r'^asset_event_logs/(\d+)/$', AssetEventLogsView.as_view(), name="asset_event_logs"),
    url(r'^get_dashboard_data/$', GetDashboardDataView.as_view(), name="get_dashboard_data"),

]