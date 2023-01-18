$(document).ready(function() {
    $("#backtest-cal").validate({
        rules: {
            protfolio_file:{
               required: true,
               extension: "xlsx"
            }
        },
        messages: {
            protfolio_file:{
                    required: "Please select input xlsx file only", 
                    extension:"Select xlsx input file format"
            } ,
        }
    });
});


toastr.options.timeOut = 300000; // 1.5s
toastr.options = {positionClass: 'toast-top-center'};
//===ajax call========//
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 
//=== ajax cal for  backtest calculation=====//
var csrftoken = getCookie('csrftoken');
 $("#backtest-cal").on('submit', function(e){
  e.preventDefault();
  if ($('#sav_data').is(":checked")){
    var name_value = document.forms["backtest-cal"]["name"].value;
    if (name_value == "") {
       $('.name-error').html('Please add porfolio name! ')
       return false;
  }
         }
         
  var formStatus = $('#backtest-cal').validate().form();
      if(true == formStatus){
         $("#myModal").modal('hide');
         var fd = new FormData();
         var files = document.getElementById('protfolio_file').files.length;
         var tax_rate = document.getElementById('tax_rate').files.length;
         for (var index = 0; index < files; index++) {
            fd.append("protfolio_file", document.getElementById('protfolio_file').files[index]);
         }
         for (var index = 0; index < tax_rate; index++) {
            fd.append("tax_rate", document.getElementById('tax_rate').files[index]);
         }
         console.log(fd);
         var name = $("#name").val();
         var currency = $("#currency").val();
         var identifier = $("#identifier").val();
         var spin_off = $("#spin_off").val();
         var index_vlaue = $("#index_vlaue").val();
         var market_value = $("#market_value").val();
         var download = $("#download").val();
         var confirmbox = $("#confirmbox").val();
         var latest_file = $("#latest_file").val();
         var save_portfolio = $('#sav_data').val();
         var tax_file_name = $('#tax_file_name').val();
         if ($('#sav_data').is(":checked")){
          var save_data ='yes';
          fd.append('save_data', save_data);
         }

         fd.append('name', name);
         fd.append('currency', currency);
         fd.append('identifier', identifier);
         fd.append('spin_off', spin_off);
         fd.append('index_vlaue', index_vlaue);
         fd.append('market_value', market_value);
         fd.append('download', download);
         fd.append('confirmbox', confirmbox);
         fd.append('latest_file', latest_file);
         fd.append('tax_file_name', tax_file_name);
         fd.append('csrfmiddlewaretoken', csrftoken);
         $.ajax({
               type: 'POST',
               url: 'calculation/portfolio/',
               data: fd,
               dataType: 'json',
               contentType: false,
               cache: false,
               processData:false,
         beforeSend: function(){
            $('.submit').attr("disabled","disabled");
            $('.loader').css('display','flex');
            toastr.info('Please Wait !');
         },
         success: function(response){
          console.log('rafi111')
            if(response.error){
              $('.msg').empty();
              $('.loader').css('display','none');
              $('.msg').html('<div class="alert alert-danger"><strong>Error! </strong>'+response.error+'</div>');
              toastr.error('Error! ' +response.error);
              $('#backtest-cal')[0].reset(); // this will reset the form fields
            }else if (response.error_msg){
                $('.msg').empty();
                $('.loader').css('display','none');
                $('.msg').html('<div class="alert alert-danger"><strong>Error! </strong>'+response.error_msg+'</div>');
                toastr.error('Error! ' +response.error_msg);
                $('#backtest-cal')[0].reset(); // this will reset the form fields
            }else if(response.warning){
               $('.msg').empty();
               $('.loader').css('display','none');
               $("#myModal").modal('show');
               $('#confirmbox').val("yes");
               $('#latest_file').val(response.file_name);
               $('#tax_file_name').val(response.tax_file_name)
               $('.warning').html('<div class="alert alert-warning"><strong>Warning! </strong>'+response.warning+'</div>');
            }else if(response.success){
               $('#alert-secondary').html(response.wrng)
               $('.msg').empty();
               $("#myModal").modal('hide');
               $('.loader').css('display','none');
               $('#backtest-cal')[0].reset();
               $(".submit").removeAttr("disabled");
               $('.backtest-cal').css('display','none');
               $('.downlaod').css('display','block');
               $("#index").attr("href", response.index_file);
               $("#constitute").attr("href", response.constituents_file);
               toastr.success('Success! ' +response.success);
            }

         }

        
      });
      }
   });
//===================ajax call for genrate existing portfolio=======//
$("#portfolio_id").change(function(e) {
  e.preventDefault()    
  var portfolio_data = new FormData();
  var portfolio = $("#portfolio_id").val();
  portfolio_data.append('id', portfolio);
  portfolio_data.append('csrfmiddlewaretoken', csrftoken);
 $.ajax({
       type: 'POST',
       url: 'calculation/get_portfolio/',
       data: portfolio_data,
       dataType: 'json',
       contentType: false,
       cache: false,
       processData:false,
         success: function(response){
          $('#stat_date').val(response.start_date);
          $('#end_date').val(response.end_date);
         }
      });
   });

//===================ajax call for rerun portfolio=======//
 $("#rerun").on('submit', function(e){
  e.preventDefault();
  if( document.rerun.portfolio_id.value == "" )
   {
     $('.rerun-msg').html('<div class="alert alert-danger" role="alert">Please select one portfolio from dropdown list.</div>')
     return false;
   }
  var rerun_data = new FormData();
  var portfolio_id = $("#portfolio_id").val();
  var stat_date = $("#stat_date").val();
  var end_date = $("#end_date").val();
  rerun_data.append('portfolio_id', portfolio_id);
  rerun_data.append('stat_date', stat_date);
  rerun_data.append('end_date', end_date);
  rerun_data.append('csrfmiddlewaretoken', csrftoken);
 $.ajax({
       type: 'POST',
       url: 'calculation/rerun_portfolio/',
       data: rerun_data,
       dataType: 'json',
       contentType: false,
       cache: false,
       processData:false,
       beforeSend: function(){
            $('.submit2').attr("disabled","disabled");
            $('.loader').css('display','flex');
            toastr.info('Please Wait !');
         },
         success: function(response){
               $('.loader').css('display','none');
               $('.down1').css('display','block');
               $('.down2').css('display','block');
               $("#rerun_index").attr("href", response.index_file);
               $("#rerun_constitute").attr("href", response.constituents_file);
               toastr.success('Success! ' +response.success);
         }
      });
   });

//=====================Ad Tax Rate===================//

 $("#addtax").on('submit', function(e){
  e.preventDefault();
  var tax_data = new FormData();
  var country = $("#country").val();
  var tax = $("#tax").val();
  tax_data.append('country', country);
  tax_data.append('tax', tax);
  console.log(tax_data)
 $.ajax({
       type: 'POST',
       url: 'calculation/add_tax/',
       data: tax_data,
       dataType: 'json',
       contentType: false,
       cache: false,
       processData:false,
       beforeSend: function(){
            $('.submitax').attr("disabled","disabled");
            $('.loader').css('display','flex');
            toastr.info('Please Wait !');            
         },
         success: function(response){
         $("#tax-myModal").modal('hide');
         $('.loader').css('display','none');
         toastr.success('Success! Tax rate is add successfully.');
         }
      });
   });

//======================Update Tax Rate=================//
$(document).ready(function(e) {
  e.preventDefault();
$('.mychoice').click(function() {
  var tax_data = new FormData();
  var mychoice = $(".mychoice").val();
  var tax = $("#tax_value_"+mychoice).val();
  var tax_id = $("#tax_id_"+mychoice).val();
  tax_data.append('tax', tax);
  tax_data.append('id', tax_id)
   $.ajax({
       type: 'POST',
       url: 'calculation/update_tax/',
       data: tax_data,
       dataType: 'json',
       contentType: false,
       cache: false,
       processData:false,
       beforeSend: function(){
            $('.loader').css('display','flex');
            toastr.info('Please Wait !');
         },
         success: function(response){
          $('.loader').css('display','none');
          $("#tax_value_"+mychoice).val(response.tax);
          $('.mychoice').prop('checked', false);
          toastr.success('Success! Tax rate is updated successfully.');
         }
      });
});
});
end_date.max = new Date().toISOString().split("T")[0];

//=======================on Slect=======//
$('#portfolio_id').change(function() {
$('#stat_date').val('');
$('#end_date').val('')
});
////
//==========================================/// 
document.getElementById("end_date").addEventListener("change", () => {
    
    var x = document.getElementById("end_date").value;
    var y = document.getElementById("stat_date").value;
    if(x<y){
      document.getElementById('end_date').value = '';
      document.getElementById("stat_date").min = x;

    }
    
});

$(".btn-danger").click(function(){
  $('#confirmbox').val('')
  $('#backtest-cal')[0].reset();
});