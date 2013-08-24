;(function($){
     window.__jot_cb_called__ = false;

     function update_objects_on_ct_change(cb){
         var content_type = $('#id_content_type');
         var object_id = $('#id_object_id');

         content_type.change(
             function(){
                 var $get = $.get(__jot_get_objects_url__+$(this).val(),
                                  function(data){
                                      object_id.html(data);
                                  })
                     .done(function(){ 
                               if( window.console ){
                                   console.log('[Jot] DEBUG: data loaded.');
                               }
                           })
                     .fail(function(){ alert( __jot_ajax_error_msg__ ); });

                 if( !window.__jot_cb_called__ && cb !== undefined && typeof(cb) == typeof(function(){}) ){
                     $get.done(cb);
                 }
             });
     }
     
     function init(){
         if( __jot_child_object_id__ ){
             update_objects_on_ct_change(
                 function(){
                     var object_id__options = $('#id_object_id').children('option');
                     object_id__options
                         .filter(':selected')
                         .removeAttr('selected');
                     $.each(object_id__options,
                            function(){
                                var $this = $(this);
                                if( $this.val() == __jot_child_object_id__){
                                    $this.attr('selected','selected');
                                }
                            });
                     window.__jot_cb_called__ = true;
                 });
             $('#id_content_type').trigger('change');
         }
         else{
             update_objects_on_ct_change();
         }
     }

     $(document).ready(init);
})(jQuery);