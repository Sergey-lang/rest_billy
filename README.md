**Entities**
- profiles - users with points,
- product - item which user can buy,
- transaction - record about sending points between users,
- order - record about user purchases (for admin* can approve or decline order),

**Scheduled task**
- add_monthly_members_points - set monthly points to 500 every 1 day of month

**Rules:**
- you can send only 100 point per month to one user,
- you can buy product only using received point,
- if you spend all monthly point and try to send points to user, system take your received points for transaction,
- every month month points set to 500 but received points will be saved,
