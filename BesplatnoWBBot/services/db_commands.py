from web.ads.models import Users, Ads, Transactions, Tariffs
from asgiref.sync import sync_to_async


@sync_to_async
def add_user(user_id, username, fullname, email, ads_amount):
	try:
		Users.objects.create(
			user_id=user_id, 
			username=username, 
			fullname=fullname,
			email=email,
			ads_amount=ads_amount
		)
	except Exception:
		pass


@sync_to_async
def select_user_by_user_id(user_id):
	user = Users.objects.filter(user_id=user_id).first()
	return user


@sync_to_async
def select_all_users():
	users = Users.objects.all()
	return users


@sync_to_async
def update_user_ads_amount(user_id, ads_amount):
	user = Users.objects.filter(user_id=user_id).first()
	user.ads_amount = ads_amount
	user.save()


@sync_to_async
def update_user_email(user_id, email):
	user = Users.objects.filter(user_id=user_id).first()
	user.email = email
	user.save()


@sync_to_async
def add_ad(user_id, text, photo, accepted, publicated, datetime_publication):
	try:
		Ads.objects.create(
			user_id=user_id, 
			text=text, 
			photo=photo,
			accepted=accepted,
			publicated=publicated,
			datetime_publication=datetime_publication
		)
	except Exception:
		pass



@sync_to_async
def select_ads_by_user_id(user_id):
	ads = Ads.objects.filter(user_id=user_id).all()
	return ads


@sync_to_async
def select_ad_by_date_and_time(datetime_publication):
	ad = Ads.objects.filter(datetime_publication=datetime_publication).first()
	return ad


@sync_to_async
def update_ad_date_and_time(ad_id, datetime_publication):
	ad = Ads.objects.filter(id=ad_id).first()
	ad.datetime_publication = datetime_publication
	ad.save()


@sync_to_async
def select_ad_by_ad_id(ad_id):
	ad = Ads.objects.filter(id=ad_id).first()
	return ad


@sync_to_async
def delete_ad_by_ad_id(ad_id):
	ad = Ads.objects.filter(id=ad_id).first()
	ad.delete()


@sync_to_async
def update_ad_accepted(ad_id):
	ad = Ads.objects.filter(id=ad_id).first()
	ad.accepted = True
	ad.save()


@sync_to_async
def update_ad_publicated(ad_id):
	ad = Ads.objects.filter(id=ad_id).first()
	ad.publicated = True
	ad.save()


@sync_to_async
def add_transaction(user_id, email, price, ads_amount, datetime_transaction):
	try:
		Transactions.objects.create(
			user_id=user_id, 
			email=email, 
			price=price,
			ads_amount=ads_amount,
			datetime_transaction=datetime_transaction
		)
	except Exception:
		pass


@sync_to_async
def select_tariffs():
	tariffs = Tariffs.objects.all()
	return tariffs