from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from content.models import ContactMessage


class Command(BaseCommand):
    help = 'حذف رسائل التواصل الأقدم من 7 أيام'

    def add_arguments(self, parser):
        # ⭐ خيار: تحديد عدد الأيام
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='عدد الأيام (افتراضي: 7)',
        )
        # ⭐ خيار: تجربة بدون حذف
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='عرض ما سيُحذف بدون حذف فعلي',
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']

        cutoff = timezone.now() - timedelta(days=days)
        old_messages = ContactMessage.objects.filter(created_at__lt=cutoff)
        count = old_messages.count()

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'[تجربة] سيتم حذف {count} رسالة أقدم من {days} يوم'
                )
            )
            return

        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('لا توجد رسائل قديمة للحذف')
            )
            return

        old_messages.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ تم حذف {count} رسالة أقدم من {days} يوم'
            )
        )