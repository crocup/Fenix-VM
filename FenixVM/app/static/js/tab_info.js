    function switchToAll() {
      removeActive();
      hideAll();
      $("#all-tab").addClass("is-active");
      $("#all-tab-content").removeClass("is-hidden");
    }
    function switchToAdaptiveDesignUpdate() {
      removeActive();
      hideAll();
      $("#adaptivedesign-tab-vulnerabilities").addClass("is-active");
      $("#adaptivedesign-tab-update-content").removeClass("is-hidden");
    }
    function removeActive() {
      $("li").each(function() {
        $(this).removeClass("is-active");
      });
    }
    function hideAll(){
      $("#all-tab-content").addClass("is-hidden");
      $("#adaptivedesign-tab-content").addClass("is-hidden");
      $("#adaptivedesign-tab-update-content").addClass("is-hidden");
    }