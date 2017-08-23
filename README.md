# rvt_fixme
a pyRevit extension to make rvt users aware of items to fix in central rvt models.
These items can be delivered either manually or automated with the upcoming version of revit_model_services.
The items are stored in an *.ini that would look like this:

```
[rvt_warnings]
warning_wall_overlaps = 333834, 333984, 334018,334019,334030,334031,334042,334043
warning_joined_not_intersect = 7934567,13453

[user_added]
username-review_join_conditions = 265838, 265865
```
