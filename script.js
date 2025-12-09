/* Small script to handle mobile nav toggle and update the summary word count when the summary placeholder changes. */
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

  // Word count for summary placeholder — updates if content changes.
  var summary = document.getElementById('summary-text');
  var wc = document.getElementById('word-count');
  function updateWordCount(){
    if(!summary || !wc) return;
    var text = summary.textContent || '';
    var words = text.trim().split(/\s+/).filter(function(w){return w.length>0});
    wc.textContent = String(words.length);
  }

  // Observe mutations in the summary placeholder to refresh the count if content is replaced.
  if(window.MutationObserver && summary){
    var mo = new MutationObserver(updateWordCount);
    mo.observe(summary, {childList:true,characterData:true,subtree:true});
  }

  // Initial count
  updateWordCount();
});
