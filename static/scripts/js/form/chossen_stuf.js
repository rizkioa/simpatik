function chosen_change(elem_){
    var siblings = elem_.nextAll('.change-related, .delete-related');
    if (!siblings.length) return;
    var value = elem_.val();
    if (value) {
        siblings.each(function(){
            var elm = $(this);
            elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
        });
    } else siblings.removeAttr('href');
}

function update_related(elm){
    if($(elm).prop( "disabled")){
        $(elm).nextAll(".change-related, .add-related").css('display', 'None')
    }else{
        $(elm).nextAll(".change-related, .add-related").css('display', 'inline-block')
    }
}

function make_disabled(elem_, dis_){
    elem_.prop( "disabled", dis_);
    elem_.trigger("chosen:updated");
    update_related(elem_)
}

function make_required(elem_, dis_){
    elem_.prop( "required", dis_);
    // elem_.trigger("chosen:updated");
    update_related(elem_)
}

function set_chosen_element(chosenEl){
    $chosenEl = $(chosenEl)
    if ($chosenEl.length > 0) {             
        $chosenEl.each(function() {
          var element = $(this);
          element.on('chosen:ready', function(e, chosen) {
            var width = element.css("width");
            element.next().find('.chosen-choices').addClass('form-control');
            element.next().css("width", width);
            element.next().find('.search-field input').css("width", "125px");
          }).chosen().change(function(data){
            //var id = $(this).val();
            $this = $(this)
            var siblings = $this.nextAll('.change-related, .delete-related');
            if (!siblings.length) return;
            var value = $this.val();
            if (value) {
                siblings.each(function(){
                    var elm = $(this);
                    elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
                });
            } else siblings.removeAttr('href');
          });                
        });
    }
}


$(".float-type").on("keyup", function(){
    var valid = /^\d{0,15}(\.\d{0,2})?$/.test(this.value),
        val = this.value;
    
    if(!valid){
        console.log("Invalid input!");
        this.value = val.substring(0, val.length - 1);
    }
});


function FormatCurrency(objNum){
 var num = objNum.value
 var ent, dec;
 if (num != '' && num != objNum.oldvalue)
 {
   num = HapusTitik(num);
   if (isNaN(num))
   {
     objNum.value = (objNum.oldvalue)?objNum.oldvalue:'';
   } else {
     var ev = (navigator.appName.indexOf('Netscape') != -1)?Event:event;
     if (ev.keyCode == 190 || !isNaN(num.split('.')[1]))
     {
       alert(num.split('.')[1]);
       objNum.value = TambahTitik(num.split('.')[0])+'.'+num.split('.')[1];
     }
     else
     {
       objNum.value = TambahTitik(num.split('.')[0]);
     }
     objNum.oldvalue = objNum.value;
   }
 }
}
function HapusTitik(num){
 return (num.replace(/\./g, ''));
}

function TambahTitik(num){
 numArr=new String(num).split('').reverse();
 for (i=3;i<numArr.length;i+=3)
 {
   numArr[i]+='.';
 }
 return numArr.reverse().join('');
} 