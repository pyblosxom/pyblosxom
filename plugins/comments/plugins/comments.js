/* AJAX comment support for pyblosxom.
 *
 * Ryan Barrett <pyblosxom@ryanb.org>
 * http://snarfed.org/space/pyblosxom+ajax+comments
 */
var xml_http_request;

function get_xmlhttpreq() {
  if (window.XMLHttpRequest) {
    xml_http_request = new XMLHttpRequest()
  } else if (window.ActiveXObject) {
    try {
      xml_http_request = new ActiveXObject("Msxml2.XMLHTTP");
    } catch(e) {
      xml_http_request = new ActiveXObject("Microsoft.XMLHTTP");
    }
  }

  return xml_http_request;
}

// remove the dom element with the given id
function remove(id) {
  elem = document.getElementById(id);
  if (elem)
    elem.parentNode.removeChild(elem);
}

// this is called by the submit buttons' onclick handlers. if it handles the
// comment ok, it returns false to tell the browser not to submit the form.
// otherwise, it returns true to tell the broser to submit the form itself.
function send_comment(type) {
  form = document.forms['comments_form'];

  // if there's already a preview or status message, delete it
  remove('comment-preview');
  remove('ajax-status');

  // validate user data
  if (type != 'post' && type != 'preview') {
    display_error('Bad comment request: ' + type);
    return false;
  }

  if (!validate_required_input('body', 'comment'))
    return false;
  else if (!validate_required_input('author', 'name'))
    return false;

  // build the XmlHttpRequest. the form's "action" is the URL to POST to.
  req = get_xmlhttpreq();
  if (!req) {
    display_error("Your browser does not support XMLHTTPRequest.");
    return true;
  }

  req.onreadystatechange = function() { comment_statechange(type); }
  req.open('POST', form.action, true);
  req.setRequestHeader('Content-type',
                       'application/x-www-form-urlencoded;charset=UTF-8');
  // build the post data
  post_data = 'ajax=' + type;
  post_data += '&' + type + '=1';

  // include all of the the form elements (for e.g. comment spam plugins)
  for (i = 0; i < form.elements.length; i++) {
    elem = form.elements[i];
    if (elem.type != 'submit' && elem.type != 'button')
      post_data += '&' + elem.name + '=' + encodeURIComponent(elem.value);
  }

  // send the request and tell the user.
  req.send(post_data);
  display_status('P' + type.substring(1) + 'ing...');
  return false;
}

function validate_required_input(name, display_name) {
  input = document.forms['comments_form'].elements[name];

  // must have at least one non-whitespace character
  if (!input.value.match('\\S')) {
    display_error('Please enter your ' + display_name + '.');
    input.style.backgroundColor = '#FFDDDD';  // pink
    return false;
  } else {
    input.style.backgroundColor = '';
    return true;
  }
}

function display_status(message) {
  p = document.createElement('p');
  p.innerHTML = '<span id="ajax-status" class="ajax-message">' +
                message + '</span>';
  anchor = document.getElementById('comment-anchor');
  anchor.parentNode.insertBefore(p, anchor);
}

function display_error(message) {
  display_status('<span class="ajax-error">' + message + '</span>');
}

function comment_statechange(type) {
  if (type != 'post' && type != 'preview') {
    display_error('Bad comment request: ' + type);
    return;
  }

  if (xml_http_request.readyState == 4) {
    remove('ajax-status');

    if (xml_http_request.responseText.length == 0) {
      display_error('Empty response from server.');
      return;
    }

    // insert the comment
    comment = document.createElement('div');
    if (type == 'preview')
      comment.setAttribute('id', 'comment-preview');
    comment.innerHTML = xml_http_request.responseText;
    anchor = document.getElementById('comment-anchor');
    anchor.parentNode.insertBefore(comment, anchor);

    if (type == 'post') {
      // clear the comment form
      form = document.getElementById('comments_form');
      for (i = 0; i < form.elements.length; i++) {
        elem = form.elements[i];
        if (elem.type != 'button' && elem.type != 'submit' &&
            elem.type != 'hidden') {
          elem.value = '';
        }
      }
    }
  }
}
