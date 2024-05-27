'browsingTopics' in document && document.featurePolicy.allowsFeature('browsing-topics') ?
 console.log('document.browsingTopics() is supported on this page') :
 console.log('document.browsingTopics() is not supported on this page');


// document.browsingTopics() returns an array of up to three topic objects in random order.


// The returned array looks like: [{'configVersion': String, 'modelVersion': String, 'taxonomyVersion': String, 'topic': Number, 'version': String}]

async function GetTopics() {
    const topics = await document.browsingTopics();
    console.log(topics); // 10
  }
  
GetTopics();



  
// // Get data for an ad creative.
// const response = await fetch('https://ads.example/get-creative', {
//   method: 'POST',
//   headers: {
//     'Content-Type': 'application/json',
//   },
//   body: JSON.stringify(topics)
// });
// // Get the JSON from the response.
// const creative = await response.json();

// Display ad.

