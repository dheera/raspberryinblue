paper-ripple
============

<<<<<<< HEAD
**This element is compatible with Polymer 0.5 and lower only, and will be deprecated.**  
You can check out a similar 0.8-compatible version of this element at [https://github.com/polymerelements/paper-input](https://github.com/polymerelements/paper-input)

See the [component page](https://www.polymer-project.org/0.5/docs/elements/paper-ripple.html) for more information.
=======
`paper-ripple` provides a visual effect that other paper elements can
use to simulate a rippling effect emanating from the point of contact.  The
effect can be visualized as a concentric circle with motion.

Example:

```html
<paper-ripple></paper-ripple>
```

`paper-ripple` listens to "mousedown" and "mouseup" events so it would display ripple
effect when touches on it.  You can also defeat the default behavior and
manually route the down and up actions to the ripple element.  Note that it is
important if you call downAction() you will have to make sure to call
upAction() so that `paper-ripple` would end the animation loop.

Example:

```html
<paper-ripple id="ripple" style="pointer-events: none;"></paper-ripple>
...
<script>
  downAction: function(e) {
    this.$.ripple.downAction({x: e.x, y: e.y});
  },
  upAction: function(e) {
    this.$.ripple.upAction();
  }
</script>
```

Styling ripple effect:

Use CSS color property to style the ripple:

```css
paper-ripple {
  color: #4285f4;
}
```

Note that CSS color property is inherited so it is not required to set it on
the `paper-ripple` element directly.


By default, the ripple is centered on the point of contact. Apply the ``recenters`` attribute to have the ripple grow toward the center of its container.

```html
<paper-ripple recenters></paper-ripple>
```

Apply `center` to center the ripple inside its container from the start.

```html
<paper-ripple center></paper-ripple>
```

Apply `circle` class to make the rippling effect within a circle.

```html
<paper-ripple class="circle"></paper-ripple>
```
>>>>>>> 31712f9c3da0221544bc5e69c1cdc4ccb22d8463
