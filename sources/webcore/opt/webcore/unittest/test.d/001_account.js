//#################
//# Account
//#################

var selector_account_form = ".x-fieldset";

cgridOpen('build','buildAccount','CPS_root')

casper.then(function() {
	casper.echo('> Fill fields and Save', 'COMMENT');
	fill_field(selector_account_form, 'user', 'casper');
	fill_field(selector_account_form, 'passwd', 'casper');
	fill_field(selector_account_form, 'firstname', 'Casper');
	fill_field(selector_account_form, 'lastname', 'JS');
	fill_field(selector_account_form, 'mail', 'capser@js.com');
	click("span.icon-save");
	waitWhile("span.icon-save");
	waitText("Casper");
	casper.waitUntilVisible("div.ui-pnotify-container");
});

cgridEditRecord(selector_account_form, 'lastname', 'Modified');

cgridRemoveRecord()

casper.then(function() {
	casper.echo('> Close Tab', 'COMMENT');
	closeTab();
});

