const countEl = document.getElementById('vc');

updateVisitCount();

function updateVisitCount() {
    fetch('https://ml28920bv7.execute-api.us-east-1.amazonaws.com/Prod/visitor_count')
        .then(response => {
        return response.json()
      })
        .then(data => {
            console.log(data)
            document.getElementById('count').innerHTML = data;
        })
    }
