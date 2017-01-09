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
