@app.route('/register.html',methods = ['POST', 'GET'])
def regis():
   if request.method == 'GET':
      return render_template('register.html')
   if request.method == 'POST':
      user_pnum = request.form.get('tt1')
      user_name=request.form.get('tt2')
      user_psd = request.form.get('tt3')
      user_sex = request.form.get('tt5')
      user_age=request.form.get('tt6')
      res=regimysql(user_pnum, user_sex, user_age, user_name, user_psd)

      if res=='well':
         data = "well"
      elif res==None:
         data = "already"
      else:
         data="wait"
      return data

@app.route('/doctorregister.html',methods = ['POST', 'GET'])
def regisdoc():
   if request.method == 'GET':
      return render_template('doctorregister.html')
   if request.method == 'POST':
      doctor_pnum = request.form.get('tt1')
      doctor_name=request.form.get('tt2')
      doctor_psd = request.form.get('tt3')
      doctor_age = request.form.get('tt5')
      doctor_field=request.form.get('tt6')
      doctor_level = request.form.get('tt7')
      doctor_worktime = request.form.get('tt8')
      res=regidocmysql(doctor_pnum, doctor_age, doctor_name, doctor_psd, doctor_field, doctor_level, doctor_worktime)
      # res=regimysql(user_pnum, user_sex, user_age, user_name, user_psd)

      if res=='well':
         data = "well"
      elif res==None:
         data = "already"
      else:
         data="wait"
      return data