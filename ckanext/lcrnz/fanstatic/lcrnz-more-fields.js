/* Module for working with multiple field inputs. This will create
 * a new field when the user changes text into the last field. It also
 * gives a visual indicator when fields are removed by disabling them.
 *
 */
this.ckan.module('lcrnz-more-fields', function (jQuery, _) {
  return {
    options: {
      /* The selector used for each custom field wrapper */
      fieldSelector: '.control-custom'
    },

    /* Initializes the module and attaches custom event listeners. This
     * is called internally by ckan.module.initialize().
     *
     * Returns nothing.
     */
    initialize: function () {
      if (!jQuery('html').hasClass('ie7')) {

        console.log('asdf');
        jQuery.proxyAll(this, /_on/);

        var delegated = this.options.fieldSelector + ':last input:first';
        this.el.on('change', delegated, this._onChange);
      }
    },

    /* Creates a new field and appends it to the list, then focus on the new field.
     * This currently works by cloning and erasing an existing input rather than
     * using a template. In future using a template might be more appropriate.
     *
     * element - Another custom field element to wrap.
     *
     * Returns nothing.
     */
    newField: function (element) {
      new_el = this.cloneField(element);
      this.el.append(new_el);
      new_el.find('input').focus();
    },

    /* Clones the provided element, wipes it's content and increments it's
     * for, id and name fields (if possible).
     *
     * current - A custom field to clone.
     *
     * Returns a newly created custom field element.
     */
    cloneField: function (current) {
      return this.resetField(jQuery(current).clone());
    },

    /* Wipes the contents of the field provided and increments it's name, id
     * and for attributes.
     *
     * field - A custom field to wipe.
     *
     * Returns the wiped element.
     */
    resetField: function (field) {
      function increment(index, string) {
        return (string || '').replace(/\d+/, function (int) { return 1 + parseInt(int, 10); });
      }

      var input = field.find(':input');
      input.val('').attr('id', increment).attr('name', increment);

      var label = field.find('label');
      label.text(increment).attr('for', increment);

      return field;
    },

    /* Disables the provided field and input elements. Can be re-enabled by
     * passing false as the second argument.
     *
     * field   - The field to disable.
     * disable - If false re-enables the element.
     *
     * Returns nothing.
     */
    disableField: function (field, disable) {
      field.toggleClass('disabled', disable !== false);
    },

    /* Event handler that fires when the last key in the custom field block
     * changes.
     */
    _onChange: function (event) {
      if (event.target.value !== '') {
        var parent = jQuery(event.target).parents(this.options.fieldSelector);
        this.newField(parent);
      }
    }
  };
});
