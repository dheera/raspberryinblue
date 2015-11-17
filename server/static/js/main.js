_ = function(q) { return document.querySelector(q); }

function doFile(e) {
  file = e.model.file;
  page(2);
  $('#iframe-viewer')[0].contentWindow.window.location.href='/static/pdfjs/web/viewer.html?file=http://cors-anywhere.herokuapp.com/http://sonatainblue.com/getfile/' + file['url'];
}

function doResultsCard(e) {
  item = e.model.item;
  getScores(item['url']);
}

function doScoresCard(e) {
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
      for(i in data) {
        if(data[i]['@type'] === 'heading' && data[i]['level'] === 3) {
          data[i]['isH3'] = true;
        }
        if(data[i]['@type'] === 'heading' && data[i]['level'] === 4) {
          data[i]['isH4'] = true;
        }
        if(data[i]['@type'] === 'heading' && data[i]['level'] === 5) {
          data[i]['isH5'] = true;
        }
        if(data[i]['@type'] === 'score') {
          data[i]['isScore'] = true;
        }
      }
      _('#scores').data=data;
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
  page(0);
  _('#input-search').addEventListener('change', function(event) {
    getSearch(event.target.value);
  });
  _('#results').data=[];
  _('#results').doResultsCard=doResultsCard;
  _('#scores').data=[];
  _('#scores').doFile=doFile;
});

// todo: build an actual Polymer component
function page(index) {
  _('.viewpager-fragments').style.WebkitTransform = 'translateX(' + (-index*100.0) + '%)';
  _('.viewpager-fragments').style.MozTransform = 'translateX(' + (-index*100.0) + '%)';
  _('.viewpager-fragments').style.msTransform = 'translateX(' + (-index*100.0) + '%)';
  _('.viewpager-fragments').style.OTransform = 'translateX(' + (-index*100.0) + '%)';
  if(index === 0) {
    _('#nav-back').style.display='none';
    _('#nav-menu').style.display='';
  } else {
    _('#nav-back').style.display='';
    _('#nav-menu').style.display='none';
  }
}

function doNavBack() {
  page(0);
}
