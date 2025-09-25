حدث خطأ أثناء حذف العميل: (sqlite3.IntegrityError) NOT NULL constraint failed: customer_payment.customer_id [SQL: UPDATE customer_payment SET customer_id=? WHERE customer_payment.id = ?] [parameters: (None, 1)] (Background on this error at: https://sqlalche.me/e/20/gkpj#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from restaurant_management import app, db
from restaurant_management.models import User, Item, Customer, Supplier, Sale, Purchase, SaleItem, PurchaseItem, CustomerPayment, Employee, SalaryPayment
from datetime import datetime, date, timedelta
import random

def create_sample_data():
    with app.app_context():
        # إنشاء قاعدة البيانات
        db.create_all()
        
        # إنشاء مستخدم admin إذا لم يكن موجوداً
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                role='admin',
                full_name='مدير النظام',
                email='admin@restaurant.com',
                phone='0501234567',
                can_manage_users=True,
                can_manage_items=True,
                can_manage_customers=True,
                can_manage_suppliers=True,
                can_manage_employees=True,
                can_manage_sales=True,
                can_manage_purchases=True,
                can_view_reports=True,
                can_manage_payments=True,
                can_delete_records=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("✅ تم إنشاء مستخدم admin")

        # إنشاء مستخدمين تجريبيين إضافيين
        sample_users = [
            {
                'username': 'manager1',
                'password': 'manager123',
                'full_name': 'أحمد المدير',
                'email': 'manager@restaurant.com',
                'phone': '0512345678',
                'role': 'manager',
                'permissions': {
                    'can_manage_items': True,
                    'can_manage_customers': True,
                    'can_manage_suppliers': True,
                    'can_manage_employees': True,
                    'can_manage_sales': True,
                    'can_manage_purchases': True,
                    'can_view_reports': True,
                    'can_manage_payments': True,
                    'can_delete_records': False
                }
            },
            {
                'username': 'cashier1',
                'password': 'cashier123',
                'full_name': 'محمد الصراف',
                'email': 'cashier@restaurant.com',
                'phone': '0523456789',
                'role': 'cashier',
                'permissions': {
                    'can_manage_sales': True,
                    'can_manage_customers': True,
                    'can_manage_payments': True,
                    'can_view_reports': False
                }
            },
            {
                'username': 'staff1',
                'password': 'staff123',
                'full_name': 'علي الموظف',
                'email': 'staff@restaurant.com',
                'phone': '0534567890',
                'role': 'staff',
                'permissions': {
                    'can_manage_sales': True
                }
            }
        ]

        for user_data in sample_users:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                permissions = user_data.pop('permissions')
                password = user_data.pop('password')

                user = User(**user_data)
                user.set_password(password)

                # تعيين الصلاحيات
                for permission, value in permissions.items():
                    setattr(user, permission, value)

                db.session.add(user)

        print("✅ تم إنشاء المستخدمين التجريبيين")
        
        # إنشاء أصناف تجريبية
        sample_items = [
            {'name': 'برجر لحم', 'price': 25.0, 'cost': 15.0, 'quantity': 50, 'category': 'وجبات رئيسية'},
            {'name': 'برجر دجاج', 'price': 22.0, 'cost': 13.0, 'quantity': 45, 'category': 'وجبات رئيسية'},
            {'name': 'بيتزا مارجريتا', 'price': 35.0, 'cost': 20.0, 'quantity': 30, 'category': 'بيتزا'},
            {'name': 'بيتزا بيبروني', 'price': 40.0, 'cost': 25.0, 'quantity': 25, 'category': 'بيتزا'},
            {'name': 'سلطة سيزر', 'price': 18.0, 'cost': 10.0, 'quantity': 40, 'category': 'سلطات'},
            {'name': 'كوكا كولا', 'price': 5.0, 'cost': 2.0, 'quantity': 100, 'category': 'مشروبات'},
            {'name': 'عصير برتقال', 'price': 8.0, 'cost': 4.0, 'quantity': 60, 'category': 'مشروبات'},
            {'name': 'قهوة عربية', 'price': 12.0, 'cost': 6.0, 'quantity': 80, 'category': 'مشروبات ساخنة'},
            {'name': 'شاي أحمر', 'price': 8.0, 'cost': 3.0, 'quantity': 90, 'category': 'مشروبات ساخنة'},
            {'name': 'كنافة', 'price': 15.0, 'cost': 8.0, 'quantity': 20, 'category': 'حلويات'},
        ]
        
        for item_data in sample_items:
            existing_item = Item.query.filter_by(name=item_data['name']).first()
            if not existing_item:
                item = Item(**item_data)
                db.session.add(item)
        
        print("✅ تم إنشاء الأصناف التجريبية")
        
        # إنشاء عملاء تجريبيين
        sample_customers = [
            {'name': 'أحمد محمد', 'phone': '0501234567', 'email': 'ahmed@example.com'},
            {'name': 'فاطمة علي', 'phone': '0507654321', 'email': 'fatima@example.com'},
            {'name': 'محمد سالم', 'phone': '0551234567', 'address': 'الرياض - حي النخيل'},
            {'name': 'نورا أحمد', 'phone': '0561234567', 'email': 'nora@example.com'},
            {'name': 'خالد عبدالله', 'phone': '0591234567', 'address': 'جدة - حي الصفا'},
        ]
        
        for customer_data in sample_customers:
            existing_customer = Customer.query.filter_by(name=customer_data['name']).first()
            if not existing_customer:
                customer = Customer(**customer_data)
                db.session.add(customer)
        
        print("✅ تم إنشاء العملاء التجريبيين")
        
        # إنشاء موردين تجريبيين
        sample_suppliers = [
            {'name': 'مؤسسة الغذاء الطازج', 'phone': '0112345678', 'email': 'fresh@supplier.com'},
            {'name': 'شركة المشروبات المتحدة', 'phone': '0123456789', 'address': 'الرياض - المنطقة الصناعية'},
            {'name': 'مورد اللحوم الطازجة', 'phone': '0134567890', 'email': 'meat@supplier.com'},
        ]
        
        for supplier_data in sample_suppliers:
            existing_supplier = Supplier.query.filter_by(name=supplier_data['name']).first()
            if not existing_supplier:
                supplier = Supplier(**supplier_data)
                db.session.add(supplier)
        
        print("✅ تم إنشاء الموردين التجريبيين")
        
        # حفظ البيانات الأساسية
        db.session.commit()
        
        # إنشاء مبيعات تجريبية
        customers = Customer.query.all()
        items = Item.query.all()
        
        if customers and items:
            # مبيعات نقدية
            for i in range(5):
                sale = Sale(
                    customer_id=None,  # عميل نقدي
                    payment_method='cash',
                    total_amount=0,
                    date=datetime.now() - timedelta(days=random.randint(0, 7))
                )
                db.session.add(sale)
                db.session.flush()
                
                # إضافة أصناف للمبيعة
                total = 0
                for j in range(random.randint(1, 3)):
                    item = random.choice(items)
                    quantity = random.randint(1, 3)
                    price = item.price
                    item_total = quantity * price
                    
                    sale_item = SaleItem(
                        sale_id=sale.id,
                        item_id=item.id,
                        quantity=quantity,
                        price=price,
                        total=item_total
                    )
                    db.session.add(sale_item)
                    total += item_total
                
                sale.total_amount = total
                sale.tax = total * 0.15 / 1.15
            
            # مبيعات آجلة
            for i in range(3):
                customer = random.choice(customers)
                sale = Sale(
                    customer_id=customer.id,
                    payment_method='credit',
                    total_amount=0,
                    date=datetime.now() - timedelta(days=random.randint(1, 10))
                )
                db.session.add(sale)
                db.session.flush()
                
                # إضافة أصناف للمبيعة
                total = 0
                for j in range(random.randint(2, 4)):
                    item = random.choice(items)
                    quantity = random.randint(1, 2)
                    price = item.price
                    item_total = quantity * price
                    
                    sale_item = SaleItem(
                        sale_id=sale.id,
                        item_id=item.id,
                        quantity=quantity,
                        price=price,
                        total=item_total
                    )
                    db.session.add(sale_item)
                    total += item_total
                
                sale.total_amount = total
                sale.tax = total * 0.15 / 1.15
            
            print("✅ تم إنشاء المبيعات التجريبية")
        
        # إنشاء مدفوعات تجريبية للعملاء
        credit_sales = Sale.query.filter_by(payment_method='credit').all()
        for sale in credit_sales[:2]:  # دفعات جزئية لأول عميلين
            payment_amount = sale.total_amount * 0.6  # دفع 60% من المبلغ
            payment = CustomerPayment(
                customer_id=sale.customer_id,
                amount=payment_amount,
                payment_method='cash',
                payment_date=sale.date + timedelta(days=random.randint(1, 5)),
                notes='دفعة جزئية',
                created_by=admin_user.id
            )
            db.session.add(payment)
        
        print("✅ تم إنشاء المدفوعات التجريبية")

        # إنشاء مشتريات تجريبية
        suppliers = Supplier.query.all()
        if suppliers and items:
            for i in range(3):
                supplier = random.choice(suppliers)
                purchase = Purchase(
                    supplier_id=supplier.id,
                    payment_method='cash',
                    total_amount=0,
                    date=datetime.now() - timedelta(days=random.randint(5, 15))
                )
                db.session.add(purchase)
                db.session.flush()

                # إضافة أصناف للمشتريات
                total = 0
                for j in range(random.randint(2, 5)):
                    item = random.choice(items)
                    quantity = random.randint(10, 50)
                    cost = item.cost
                    item_total = quantity * cost

                    purchase_item = PurchaseItem(
                        purchase_id=purchase.id,
                        item_id=item.id,
                        quantity=quantity,
                        cost=cost,
                        total=item_total
                    )
                    db.session.add(purchase_item)
                    total += item_total

                    # تحديث المخزون
                    item.quantity += quantity

                purchase.total_amount = total
                purchase.tax = total * 0.15 / 1.15

            print("✅ تم إنشاء المشتريات التجريبية")

        # إنشاء موظفين تجريبيين
        sample_employees = [
            {
                'name': 'أحمد محمد علي',
                'residence_number': '2345678901',
                'nationality': 'سعودي',
                'position': 'طباخ',
                'monthly_salary': 4500.00,
                'phone': '0501234567',
                'address': 'الرياض - حي النخيل'
            },
            {
                'name': 'محمد أحمد حسن',
                'residence_number': '3456789012',
                'nationality': 'مصري',
                'position': 'مقدم طعام',
                'monthly_salary': 3200.00,
                'phone': '0512345678',
                'address': 'الرياض - حي الملز'
            },
            {
                'name': 'عبدالله سالم محمد',
                'residence_number': '4567890123',
                'nationality': 'يمني',
                'position': 'صراف',
                'monthly_salary': 3800.00,
                'phone': '0523456789',
                'address': 'الرياض - حي العليا'
            },
            {
                'name': 'خالد عبدالرحمن',
                'residence_number': '5678901234',
                'nationality': 'سعودي',
                'position': 'مدير',
                'monthly_salary': 6000.00,
                'phone': '0534567890',
                'address': 'الرياض - حي الورود'
            },
            {
                'name': 'عمر حسين علي',
                'residence_number': '6789012345',
                'nationality': 'سوري',
                'position': 'مساعد طباخ',
                'monthly_salary': 2800.00,
                'phone': '0545678901',
                'address': 'الرياض - حي الشفا'
            }
        ]

        for emp_data in sample_employees:
            existing_employee = Employee.query.filter_by(residence_number=emp_data['residence_number']).first()
            if not existing_employee:
                employee = Employee(**emp_data)
                db.session.add(employee)

        print("✅ تم إنشاء الموظفين التجريبيين")

        # حفظ البيانات قبل إنشاء مدفوعات الرواتب
        db.session.commit()

        # إنشاء بعض مدفوعات الرواتب التجريبية
        employees = Employee.query.all()
        current_date = date.today()

        for employee in employees:
            # دفع راتب الشهر الماضي
            last_month = current_date.month - 1 if current_date.month > 1 else 12
            last_year = current_date.year if current_date.month > 1 else current_date.year - 1

            salary_payment = SalaryPayment(
                employee_id=employee.id,
                amount=employee.monthly_salary,
                salary_month=last_month,
                salary_year=last_year,
                payment_method='cash',
                payment_date=date(last_year, last_month, 28),
                notes=f'راتب شهر {last_month}/{last_year}',
                created_by=admin_user.id
            )
            db.session.add(salary_payment)

        print("✅ تم إنشاء مدفوعات الرواتب التجريبية")

        # حفظ جميع البيانات
        db.session.commit()

        print("🎉 تم إنشاء جميع البيانات التجريبية بنجاح!")
        print(f"📊 الإحصائيات:")
        print(f"   - المستخدمين: {User.query.count()}")
        print(f"   - الأصناف: {Item.query.count()}")
        print(f"   - العملاء: {Customer.query.count()}")
        print(f"   - الموردين: {Supplier.query.count()}")
        print(f"   - الموظفين: {Employee.query.count()}")
        print(f"   - المبيعات: {Sale.query.count()}")
        print(f"   - المشتريات: {Purchase.query.count()}")
        print(f"   - مدفوعات العملاء: {CustomerPayment.query.count()}")
        print(f"   - مدفوعات الرواتب: {SalaryPayment.query.count()}")
        print("\n🔑 معلومات تسجيل الدخول:")
        print("   اسم المستخدم: admin")
        print("   كلمة المرور: admin123")

if __name__ == '__main__':
    create_sample_data()
