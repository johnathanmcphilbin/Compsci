/* Small script to handle mobile nav toggle. */
document.addEventListener('DOMContentLoaded', function(){
  var navToggle = document.getElementById('nav-toggle');
  var primaryNav = document.getElementById('primary-nav');
  if(navToggle && primaryNav){
    navToggle.addEventListener('click', function(){
      var isOpen = primaryNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });

    // Close nav when a link is clicked (mobile)
    primaryNav.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){
        primaryNav.classList.remove('open');
        navToggle.setAttribute('aria-expanded','false');
      });
    });
  }

  // Smooth scroll for same-page anchors
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor){
    anchor.addEventListener('click', function(e){
      var targetId = this.getAttribute('href').slice(1);
      var target = document.getElementById(targetId);
      if(target){
        e.preventDefault();
        target.scrollIntoView({behavior:'smooth',block:'start'});
      }
    });
  });
});
