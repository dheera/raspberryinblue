_ = function(q) { return document.querySelector(q); }

function doResultsCard(e) {
  item = e.model.item;
  getScores(item['url']);
}

function getScores(url) {
  page(1);
  _('#div-scores-spinner').style.display='';
  _('#scores').data = [];
  $.get(
    '/scores',
    {
      'url':url
    },
    function(data, textStatus, jqXHR) {
      _('#div-scores-spinner').style.display='none';
      _('#scores').data=data;
      console.log(data);
    },
    'json'
  );
}

function getSearch(q) {
  _('#div-results-spinner').style.display='';
  _('#results').data = [];
  $.get(
    '/search',
    {
      'q':q
    },
    function(data, textStatus, jqXHR) {
      _('#div-results-spinner').style.display='none';
      _('#results').data=data;
    },
    'json'
  );
}

$(function() {
  _('#input-search').addEventListener('change', function(event) {
    getSearch(event.target.value);
  });
  _('#results').data=[];
  _('#results').doResultsCard=doResultsCard;
  _('#scores').data=[];
});

// todo: build an actual Polymer component
function page(index) {
  _('.viewpager-fragments').style.webkitTransform = 'translateX(' + (-index*50) + '%)';
}
