$(function() {
        var submitresult = {{ submit_result }};
        console.log(submitresult);
        if (submitresult == 100){
            submitresult = 0;
            $('#welcomeModal').modal('show');
        }if (submitresult == 200){
            submitresult = 0;
            alert('注册失败，请联系管理员');
        }

        var timewait = 60;
        function countdown() {
            if (timewait == 0){
                $('#sendshortmessage').attr({disabled: false});
                $('#sendshortmessage').html('发送验证码');
                clearTimeout(countdown);
                timewait = 60;
            }
            else{
                $('#sendshortmessage').attr({disabled: true});
                $('#sendshortmessage').html(timewait + ' 秒...  ');
                timewait -- ;
                setTimeout(countdown, 1000);
            }
        }

         var phone_number;
         var invalid_phone = false;
        $('#sendshortmessage').click(function () {
            phone_number = $('#phonenumber').val();
            if (phone_number == ''){
                $('#phonenumber').addClass("is-invalid");
                $('.col-7').append("<div class=\"invalid-feedback\">&ensp;请输入手机号</div>");

            }
            else{
                $('#phonenumber').removeClass("is-invalid");
                $('.col-7 .invalid-feedback').remove();
                if (invalid_phone == false){
                    var url = "{{ url_for('validcode') }}";
                    $.get(url, {phone:phone_number});
                    countdown();
                }
            }
        });

        $('#phonenumber').click(function () {
            $('#phonenumber').removeClass("is-invalid");
            $('.col-7 .invalid-feedback').remove();
            $('#sendshortmessage').attr({disabled: false});
        });

        $("#province").ready(function () {
            $.get(Flask.url_for('provinces')).done(function (data) {
                var option_html = "";
                $.each(data, function (idx, obj) {
                    option_html = option_html + "<option value=\"" + obj.id + "\">" + obj.name + "</option>";
                    $('#province').html(option_html);
                });
            });
        });

        $("#province").change(function () {
            var p_id = $('#province option:selected').val();
            $.get(Flask.url_for('regions'), {province: p_id}).done(function (data) {
                var option_html = "";
                $.each(data, function (idx, obj) {
                    option_html = option_html + "<option value=\"" + obj.id + "\">" + obj.name + "</option>";
                    $('#city').html(option_html);
                });
            });
        });

        $("#city").change(function () {
            var c_id = $('#city option:selected').val();
            $.get(Flask.url_for('regions'), {city: c_id}).done(function (data) {
                var option_html = "";
                $.each(data, function (idx, obj) {
                    option_html = option_html + "<option value=\"" + obj.id + "\">" + obj.name + "</option>";
                    $('#district').html(option_html);
                });
            });
        });


        var validator = $('#registerForm').validate({
            rules:{
            province:"required",
            city:"required",
            district:"required",
            endpoint:"required",
            name:"required",
            phonenumber:{
                required:true,
                phone_check:true
            },
            gender:"required",
            validcode:{
              required:true,
              code_valid:true
            }

          },
          messages:{
            province:"请选择省",
            city:"请选择市",
            district:"请选择区",
            endpoint:"请输入终端名称",
            name:"请输入姓名",
            phonenumber:{
                required:"请输入手机号",
                phone_check:"此手机号已注册"
            },
            validcode:{
              required:"请输入验证码",
              code_valid:"验证码错误"
            },
            gender:"请选择性别"
          },
           errorPlacement: function(error, element) {      //错误信息的位置
            error.appendTo( element.parent() );
          }

        });

        $.validator.addMethod('code_valid', function (value, element) {
            var result;
            var code_str = '/' + value + '/';
            var url = Flask.url_for('code_validate', code=value).replace('//', code_str);
            $.ajax({
                url:url,
                async: false,
                type:'get',
                success:function (data) {
                    result = data.status;
                }

            });
            if (result == '100'){
                return true
            }else{
                return false
            }

        }, 'code wrong !');

        $.validator.addMethod('phone_check', function (value, element) {
            var result;
            var phone_str = '/' + value + '/';
            var url = Flask.url_for('phone_check', phone=value).replace('//', phone_str);
            $.ajax({
                url:url,
                async: false,
                type:'get',
                success:function (data) {
                    result = data.status;
                }

            });
            if (result == '100'){
                invalid_phone = false;
                return true
            }else{
                console.log('aaaainvalid_phone = ' + invalid_phone);
                invalid_phone = true;
                return false
            }

        }, 'phone number duplicated !');

    $("#submitbutton").click(function(){
            $('.col-7 .invalid-feedback').remove();
            $('#registerForm').submit();

        })
    });