# -*- coding: utf-8 -*-
##############################################################################

#
##############################################################################

from odoo import fields, models ,api, _
from tempfile import TemporaryFile
from openerp.exceptions import UserError, ValidationError
from datetime import  datetime
from odoo.exceptions import UserError
from odoo import api, exceptions, fields, models, _
#from datetime import  timedelta
from odoo.tools import misc, DEFAULT_SERVER_DATETIME_FORMAT
import base64
import copy
import datetime
import io
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from datetime import date
from calendar import monthrange
import string 
import random
from dateutil.relativedelta import relativedelta
import xlrd
import collections
from collections import Counter
from xlrd import open_workbook
import csv
import base64
import sys
# from odoo import pycompat
import datetime
import calendar
#import unicodecsv


class MemberAppAuto_wizard(models.TransientModel):
    _name = 'member_auto.wizard'

    select_file = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select')
    # crt_upt_file = fields.Selection([('create', 'Create Product'), ('update', 'Update Product')], string='Import Type')
    data_file = fields.Binary(string="File")
 

    @api.multi
    def Import_Membership(self):
        partner_obj = self.env['res.partner'] 
        member_obj = self.env['member.app']
         
        if self.select_file and self.data_file:
            if self.select_file == 'csv':
                fileobj = TemporaryFile('w+')
                fileobj.write(base64.decodestring(self.data_file))
                fileobj.seek(0)
                reader = csv.reader(fileobj, delimiter=',', quotechar="'", dialect=csv.excel_tab)
                next(reader)
                file_data = reader
            elif self.select_file == 'xls':
                file_datas = base64.decodestring(self.data_file)
                workbook = xlrd.open_workbook(file_contents=file_datas)
                sheet = workbook.sheet_by_index(0)
                result = []
                data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
                data.pop(0)
                file_data = data
        else:
            raise exceptions.Warning(_('Please select file and type of file'))

        for row in file_data:
            try:
                member_name = str(row[1] +' '+ row[0]+' '+row[3])
                member_search = member_obj.search([('partner_id.name', '=ilike', member_name)], limit=1)
                
                list_sponsor = []
                list_nok =[] 
                sponsor1 = [row[18], row[19]] 
                nok_search = member_obj.search([('partner_id.name', '=ilike', row[5])], limit=1)
                if not nok_search:
                    partner = partner_obj.create({'name': row[5],
                                                'phone': row[7],
                                                'email': row[8],
                                                'street': row[6]})
                    list_nok.append(partner.id)
                else:
                    list_nok.append(nok_search.id)
                
                for lists in sponsor1:
                    search_partner = partner_obj.search([('name', '=ilike', lists)], limit=1)
                    if not search_partner:
                        partner = partner_obj.create({'name': lists,
                                                    'phone': 'Null',
                                                    'email': 'Null',
                                                    'street': 'Null'})
                        list_sponsor.append(partner.id)
                    else:
                        list_sponsor.append(search_partner.id)
                        
                search_part = partner_obj.search([('name', '=ilike', member_name)], limit=1)
                part_id = []
                if not search_part:
                    partner = partner_obj.create({'name': str(row[1] +' '+ row[0]),
                                                'phone':row[13],
                                                'email':row[12],
                                                'street':row[4]}) 
                    part_id.append(partner.id)
                else:
                    part_id.append(search_part.id) 
                        
                country_obj = self.env['res.country']
                search_country = country_obj.search([('name', '=ilike', row[3])], limit=1)
                
                country_list = []
                if not search_country:
                    country = country_obj.create({'name': row[3]}) # raise ValidationError("partner ids  '%s' not found" % row[2])
                    country_list.append(country.id)
                else:
                    country_list.append(search_country.id)
                
                if not member_search:
                    member_id = member_obj.create({'surname':row[0],
                                                'partner_id': self.env['res.partner'].browse(part_id).id, 
                                                'first_name': row[1],
                                                'middle_name':str(row[2]) + ' ',
                                                'country_id': self.env['res.country'].browse(country_list).id,
                                                'street': row[4],
                                                'nok': self.env['res.partner'].browse(list_nok).id,
                                                'nok_address_work': row[6],
                                                'state':row[9],
                                                'place_of_work': row[10],
                                                'position_holder':row[11], 
                                                'email': row[12],
                                                'phone': row[13], 
                                                'dob': row[14],  # fields.Datetime.now(),
                                                'date_order': row[15],
                                                'sex': row[16],
                                                'marital_status':row[17], 
                                                'sponsor': [(4, list_sponsor)],
                                                'identification': row[20], 
                                                'city': row[21],
                                                'active': row[22],                                               
                                                'email_work': row[23], 
                                                    
                                                
                                                })
                else:
                    # member_search.write({'state': row[9],
                    #                      'active':row[22],
                    #                      'phone':row[13],
                    #                      'email': row[12],
                    #                      'phone': row[13], 
                    #                      'email':row[12],
                    #                      'identification':row[20], 
                    #                      'marital_status':row[17], 
                    #                      'city':row[21],
                    #                      'place_of_work': row[10],
                    #                      'position_holder':row[11]
                    #                      })
                    raise ValidationError('Member Already Exist')
            except Exception as error:
                print('Caught this error: ' + repr(error))
                raise ValidationError('There is a problem with record {}. Check the error around Column: {}' .format(row, error))


class MemberAppAuto_wizard(models.TransientModel):
    _name = 'member.dependant.wizard'

    select_file = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select')
    data_file = fields.Binary(string="File")

    @api.multi
    def Import_Dependants(self):
        partner_obj = self.env['res.partner'] 
        member_obj = self.env['member.app']
         
        if self.select_file and self.data_file:
            if self.select_file == 'csv':
                fileobj = TemporaryFile('w+')
                fileobj.write(base64.decodestring(self.data_file))
                fileobj.seek(0)
                reader = csv.reader(fileobj, delimiter=',', quotechar="'", dialect=csv.excel_tab)
                next(reader)
                file_data = reader
            elif self.select_file == 'xls':
                file_datas = base64.decodestring(self.data_file)
                workbook = xlrd.open_workbook(file_contents=file_datas)
                sheet = workbook.sheet_by_index(0)
                result = []
                data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
                data.pop(0)
                file_data = data
        else:
            raise exceptions.Warning(_('Please select file and type of file'))

        for row in file_data:
            try:
                member_name = str(row[2] +' '+ row[3])
                dependant_name = str(row[2] +' '+ row[3])
                depend_obj = self.env['register.spouse.member']
                depend_search = depend_obj.search([('partner_id.name', '=ilike', dependant_name)], limit=1)
                
                member_search = member_obj.search([('identification', '=ilike', row[0])], limit=1)
                
                search_part = partner_obj.search([('name', '=ilike', dependant_name)], limit=1)
                part_id = []
                if not search_part:
                    partner = partner_obj.create({'name': str(row[2] +' '+ row[3]),
                                                'phone':row[7],
                                                'email':row[8],
                                                'street':row[10]}) 
                    part_id.append(partner.id)
                else:
                    part_id.append(search_part.id) 
                        
                country_obj = self.env['res.country']
                search_country = country_obj.search([('name', '=ilike', row[3])], limit=1)
                
                country_list = []
                if not search_country:
                    country = country_obj.create({'name': row[11]}) # raise ValidationError("partner ids  '%s' not found" % row[2])
                    country_list.append(country.id)
                else:
                    country_list.append(search_country.id)
                
                if not depend_search:
                    member_depend_id = depend_obj.create({'surname':row[2],
                                                'partner_id': self.env['res.partner'].browse(part_id).id, 
                                                'first_name': row[3],
                                                'country_id': self.env['res.country'].browse(country_list).id,
                                                'street': row[10],
                                                'email': row[7],
                                                'phone': row[8], 
                                                'dob': row[5],  # fields.Datetime.now(),
                                                'date_order': fields.Datetime.now(),
                                                'sex': row[6],
                                                'marital_status':row[12],
                                                'identification': row[9],
                                                'relationship':row[13],
                                                'account_id':1,
                                                #'nok': self.env['res.partner'].browse(list_nok).id,
                                                # 'nok_address_work': row[6],
                                                # 'state':row[9],
                                                # 'place_of_work': row[10],
                                                #'position_holder':row[11], 
                                                # 'sponsor': [(4, list_sponsor)], 
                                                #'city': row[21],
                                                #'active': row[22],                                               
                                                # 'email_work': row[23], 
                                                })
                    dp_list.append(member_depend_id).id
                    
                else:
                    
                    raise ValidationError('Dependant Already Exist')
                try:
                    if member_search:
                        member_search.write({'depend_name': [(4,dp_list)]})
                except Exception as error:
                    print('Caught this Issue: ' + repr(error))
                    raise ValidationError('The member in around row {} does not exit. Read the trackback error {}' .format(row, error))
    
            except Exception as error:
                print('Caught this error: ' + repr(error))
                raise ValidationError('There is a problem with record {}. Check the error around Column: {}' .format(row, error))


class AutoChartOfAccountwizard(models.TransientModel):
    _name = 'chart_autoaccount.wizard'
    select_file = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select')
    data_file = fields.Binary(string="File")
 
    @api.multi
    def ImportChartAccount(self):
        account_type_obj = self.env['account.account.type']
        account_obj = self.env['account.account']
        
         
        if self.select_file and self.data_file:
            if self.select_file == 'csv':
                fileobj = TemporaryFile('w+')
                fileobj.write(base64.decodestring(self.data_file))
                fileobj.seek(0)
                reader = csv.reader(fileobj, delimiter=',', quotechar="'")
                next(reader)
                file_data = reader
            elif self.select_file == 'xls':
                file_datas = base64.decodestring(self.data_file)
                workbook = xlrd.open_workbook(file_contents=file_datas)
                sheet = workbook.sheet_by_index(0)
                result = []
                data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
                data.pop(0)
                file_data = data
        else:
            raise exceptions.Warning(_('Please select file and type of file'))

        for row in file_data:
            accounts = account_obj.search([('name','=',row[0])], limit=1)
            accounts_type = account_type_obj.search([('name','=',row[1])], limit=1)
            account_id = 0
            account_type_id = 0
            if not accounts: 
                if not accounts_type:
                    acc_type = account_type_obj.create({'name':row[1]})
                    account_type_id = acc_type.id
                else: 
                    account_type_id = accounts_type.id
                    
                accounut_ids = account_obj.create({
                                                    'name':row[0], 
                                                    'user_type_id': account_type_id,
                                                    'code':row[2],
                                                    })
                
            else:
                
                accounts.write({
                                'code':row[2],
                                #'user_type_id': account_type_id,
                                       })
                
class AutoHRwizard(models.TransientModel):
    _name = 'hr_employeeauto.wizard'
    select_file = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select')
    data_file = fields.Binary(string="File")
 
    @api.multi
    def ImportEmployee(self):
        employee_obj = self.env['hr.employee']
        department_obj = self.env['hr.department']
        job_obj = self.env['hr.job']
        
         
        if self.select_file and self.data_file:
            if self.select_file == 'csv':
                fileobj = TemporaryFile('w+')
                fileobj.write(base64.decodestring(self.data_file))
                fileobj.seek(0)
                reader = csv.reader(fileobj, delimiter=',', quotechar="'")
                next(reader)
                file_data = reader
            elif self.select_file == 'xls':
                file_datas = base64.decodestring(self.data_file)
                workbook = xlrd.open_workbook(file_contents=file_datas)
                sheet = workbook.sheet_by_index(0)
                result = []
                data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
                data.pop(0)
                file_data = data
        else:
            raise exceptions.Warning(_('Please select file and type of file'))

        for row in file_data:
            employee = employee_obj.search([('name','=',row[0])], limit=1)
            department = department_obj.search([('name','=',row[1])], limit=1)
            job = job_obj.search([('name','=',row[2])], limit=1)
            department_id = 0
            job_id = 0
            if not employee: 
                if not department:
                    dept = department_obj.create({'name':row[1]})
                    department_id = dept.id
                else: 
                    department_id = department.id 
                
                if not job:
                    jb = job_obj.create({'name':row[2], 'department_id':department_id})
                    job_id = jb.id
                else: 
                    job_id = job.id 
                    
                employee_ids = employee_obj.create({
                                                    'name':row[0], 
                                                    'department_id': department_id,
                                                    'job_id': job_id
                                                    # 'unit_emp':1,
                                                     
                                                    })
                
            else:
                employee.write({
                                'name':row[0], 
                                'department_id': department_id,
                                       })
                


class Account_payment(models.TransientModel):
    _name = 'payment_auto.wizard'

    select_file = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select') 
    data_file = fields.Binary(string="File") 
    confirm_state = fields.Selection([('draft', 'Draft'), ('post', 'Post')], string='Select', required=True) 
    

    @api.multi
    def Import_AccountPayment(self):
        partner_obj = self.env['res.partner']
        user_obj = self.env['res.users'] 
        branch_obj = self.env['res.branch'] 
        payment_obj = self.env['account.payment'] 
        journal = self.env['account.journal'] 
        if self.select_file and self.data_file:
            if self.select_file == 'csv':
                fileobj = TemporaryFile('w+')
                fileobj.write(base64.decodestring(self.data_file))
                fileobj.seek(0)
                reader = csv.reader(fileobj, delimiter=',', quotechar="'")
                next(reader)
                file_data = reader
            elif self.select_file == 'xls':
                file_datas = base64.decodestring(self.data_file)
                workbook = xlrd.open_workbook(file_contents=file_datas)
                sheet = workbook.sheet_by_index(0)
                result = []
                data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
                data.pop(0)
                file_data = data
        else:
            raise exceptions.Warning(_('Please select file and type of file'))
        
        journal_list = []
        
        code = "i"
        result = "o"
        if len(code) < 6:
            letters = string.ascii_letters
            nums = string.digits
            char =(''.join(random.choice(letters) for i in range(3)))
            number = (''.join(random.choice(nums) for i in range(3)))
            result = char+number
            result = result.upper()
            num = 12345678
        for row in file_data:
            
            ############## Create account ##########
            # char = string.ascii_letters 
            # number = string.digits
            # letter = (''.join(random.choice(char) for i in range(3)))
            # nums = (''.join(random.choice(number) for i in range(3)))
            # resu = letter + nums
            # result = resu.upper()
            debit_account = []
            credit_account = []
            account_obj = self.env['account.account']
            search_debit_account = account_obj.search([('name', '=ilike', row[4])], limit=1)
            search_part = partner_obj.search([('name', '=ilike', row[0])], limit=1)
            search_journal = journal.search([('name', '=ilike', row[2])], limit=1)
            
            if not search_debit_account:
                # CREDIT Account
                account_id = account_obj.create({
                                                'code': row[4][0:3], 
                                                'user_type_id':self.env['account.account.type'].search([('name','=','Expenses')]).id, 
                                                'name': row[4], 
                                                 })
                debit_account.append(account_id.id)
            else:
                debit_account.append(search_debit_account.id)
                
            search_credit_account = account_obj.search([('name', '=ilike', row[5])], limit=1)
            if not search_credit_account:
                # CREDIT account
                account_id = account_obj.create({
                                                'code': row[5][0:3], 
                                                'user_type_id':self.env['account.account.type'].search([('name','=','Income')]).id, 
                                                'name': row[5], 
                                                 })
                credit_account.append(account_id.id)
            else:
                credit_account.append(search_credit_account.id)
                
            part_id = []
            if not search_part:
                partner = partner_obj.create({'name': row[0],
                                              }) # raise ValidationError("partner ids  '%s' not found" % row[2])
                part_id.append(partner.id)
            else:
                part_id.append(search_part.id) 
               
            if not search_journal:
                journal_id = journal.create({'name': row[2], 
                                              'type': row[3], 
                                              'default_debit_account_id': self.env['account.account'].browse(debit_account).id, 
                                              'default_credit_account_id':self.env['account.account'].browse(credit_account).id,
                                              'code': row[2][0:3]
                                              })
                journal_list.append(journal_id.id)
            else:
                journal_list.append(search_journal.id)

            account_payment_obj = self.env['account.payment.method']
            search_acm = account_payment_obj.search([('name', '=ilike', row[10])], limit=1)
            acm_list = []
            if not search_acm:
                account_method_id = account_payment_obj.create({
                                                                'payment_type': 'inbound',
                                                                'name': row[10],
                                                                'code': row[10][0:3],
                                                                })
                acm_list.append(account_method_id.id)
            else:
                acm_list.append(search_acm.id)
                
            payment_data = {
                'amount': row[1],
                'payment_date': row[7],
                'partner_type': row[9], # 'customer',
                'payment_type': row[8], # 'inbound',
                'partner_id': row[0],
                'partner_id': self.env['res.partner'].browse(part_id).id,
                'journal_id': self.env['account.journal'].browse(journal_list).id,
                'narration': row[6],
                'communication': row[6],
                'payment_method_id':self.env['account.payment.method'].browse(acm_list).id, 
                            }
            payment_model = payment_obj.create(payment_data)
             



           
    
            
              