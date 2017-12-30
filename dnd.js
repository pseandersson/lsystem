"use strict"
function DragAndDropHelper(container, classname, horizontal) {
    // Internal static variables to keep track of items
    if (DragAndDropHelper.mode === undefined)
        DragAndDropHelper.mode = null;
    if (DragAndDropHelper.hover_item === undefined)
        DragAndDropHelper.hover_item = null;
    if (DragAndDropHelper.drag_item === undefined)
        DragAndDropHelper.drag_item = null;
    if (DragAndDropHelper.registered_ids === undefined)
        DragAndDropHelper.registered_ids = [];
    if (DragAndDropHelper.index_count === undefined)
        DragAndDropHelper.index_count = 0;
    if (DragAndDropHelper.current_item_rect === undefined)
        DragAndDropHelper.current_item_rect = null;

    this.horizontal = (horizontal !== undefined)? horizontal : true;

    // Drop container
    this.dropContainer = document.getElementById(container);
    this.itemClassname = classname;

    // Regular expressions for matching classes and values
    const val_pat = /([+-]?[0-9\.]+)(%|[a-z]+)*/i;
    const highlight_pat = / highlight\b/;
    const ondrag_pat = / ondrag\b/;

    // Mode constants
    const ADD = "add";
    const REARRANGE = "rearrange";

    this.allowDrop = function(ev) {
        ev.preventDefault();
        var current_obj;
        var width;
        var height;
        var highlight_element = false;

        // Loop through all elements to see if
        // and subitems are matched
        Array.from(this.dropContainer.children).forEach( function(value) {
            // Skip if same or if current_obj found
            if (DragAndDropHelper.drag_item === value || current_obj !== undefined)
                return;
            var rect = value.getBoundingClientRect();
            // Convert margin to number
            var lm = val_pat.exec(value.style.marginLeft);
            var tm = val_pat.exec(value.style.marginTop);
            var rm = 0;
            var bm = 0;
            // Compensate for left margin
            if (lm === null)
                lm = 0;
            else {
                lm =  (lm[2] == "em") ? lm[1]*16 : lm[1];
                rm = (lm > 0 ) ? rect.width / 2 : 0;
            }
            // Compensate for top margin
            if (tm === null)
                tm = 0;
            else {
                tm =  (tm[2] == "em") ? tm[1]*16 : tm[1];
                bm = (tm > 0) ?  rect.height / 2 : 0;
            }

            // check if it's occupying the item
            if (ev.x >= rect.left-lm &&
                ev.x <= rect.right-rm &&
                ev.y >= rect.top-tm &&
                ev.y <= rect.bottom-bm)
            {
                highlight_element = (ev.x >= rect.left && this.horizontal === true || ev.y >= rect.top && this.horizontal === false);

                width = DragAndDropHelper.current_item_rect.width;
                height = DragAndDropHelper.current_item_rect.height;
                current_obj = value;
            }
        }.bind(this));

        // Update state of hovered items
        if (current_obj != DragAndDropHelper.hover_item) {
            if (DragAndDropHelper.hover_item != null) {
                DragAndDropHelper.hover_item.style.marginLeft = "0px";
                DragAndDropHelper.hover_item.style.marginTop = "0px";
                lowlight(DragAndDropHelper.hover_item);
            }

            DragAndDropHelper.hover_item = current_obj;

            if (DragAndDropHelper.hover_item != null) {
                if (this.horizontal) {
                    DragAndDropHelper.hover_item.style.marginLeft = width + "px";
                } else {
                    DragAndDropHelper.hover_item.style.marginTop = height + "px";
                }
            }
        }
        // If in add mode, then always update highlight
        if ((DragAndDropHelper.mode === ADD ||
            (DragAndDropHelper.mode === REARRANGE &&
             DragAndDropHelper.drag_item.parentElement !== this.dropContainer))
              && DragAndDropHelper.hover_item != null) {
            if (highlight_element) {
                highlight(DragAndDropHelper.hover_item);
            } else {
                lowlight(DragAndDropHelper.hover_item);
            }
        }
    }

    function highlight(element) {
        if (!element.className.includes(" highlight"))
            element.className = element.className + " highlight";
    }

    function lowlight(element) {
        element.className = element.className.replace(highlight_pat,"");
    }

    this.drag = function(ev) {
        ev.dataTransfer.setData("text", ev.target.id);
        DragAndDropHelper.current_item_rect = ev.target.getBoundingClientRect();
        DragAndDropHelper.mode = ADD;
    }

    this.dragAndArrange = function (ev) {
        ev.dataTransfer.setData("text", ev.target.id);
        DragAndDropHelper.drag_item = ev.target;
        DragAndDropHelper.current_item_rect = ev.target.getBoundingClientRect();
        // We have to hide it so the other
        // items can occupy the chosen items place
        DragAndDropHelper.drag_item.className += " ondrag";
        // set mode
        DragAndDropHelper.mode = REARRANGE;
    }

    this.removeItem = function(ev) {
        var target = this.getValidTarget(ev.target);
        var id = [];
        DragAndDropHelper.registered_ids.splice(id.indexOf(target.id), 1);
        if (target !== null)
            target.parentElement.removeChild(target);
    }

    this.drop = function(ev) {
        ev.preventDefault();
        var lMode = DragAndDropHelper.mode;
        DragAndDropHelper.mode = null;
        ev.dataTransfer.dropEffect = "none"

        var id = ev.dataTransfer.getData("text");
        var node = document.getElementById(id);

        if (node == null)
            return;

        // if not the main container then
        // we shall query for replacement

        if (lMode === ADD)
            if ((ev.target.id !== this.dropContainer.id))
                this.replace(ev, this.newNode(node))
            else
                this.add(ev, node);
        else if (lMode === REARRANGE)
            if ((DragAndDropHelper.drag_item.parentElement !== this.dropContainer) &&
                (ev.target.id !== this.dropContainer.id))
                    this.replace(ev, node)
            else
                this.arrange(ev, node)
    }

    this.resetDrag = function(event) {
        // Clear up the static variables
        if (DragAndDropHelper.hover_item != null) {
            DragAndDropHelper.hover_item.style.marginLeft = "0em";
            DragAndDropHelper.hover_item.style.marginTop = "0em";
            lowlight(DragAndDropHelper.hover_item);
            DragAndDropHelper.hover_item = null;
        }
        if (DragAndDropHelper.drag_item !== null) {
            DragAndDropHelper.drag_item.className = DragAndDropHelper.drag_item.className.replace(ondrag_pat, "");
            DragAndDropHelper.drag_item = null;
        }
        if (DragAndDropHelper.current_item_rect !== null) {
            DragAndDropHelper.current_item_rect = null;
        }
    }

    this.newNode = function(node) {
        var element = node.cloneNode(true);
        element.addEventListener("dragstart", function(e) { this.dragAndArrange(e); }.bind(this), false);
        element.addEventListener("dragend", function(e) { this.resetDrag(e); }.bind(this), false);
        element.addEventListener("click", function(e) { this.removeItem(e); }.bind(this), false);
        element.setAttribute("id", this.dropContainer.id + "__item__" + DragAndDropHelper.index_count++);
        DragAndDropHelper.registered_ids.push(element.id);
        return element;
    }

    this.add = function(ev, node) {
        var element = this.newNode(node);
        if (DragAndDropHelper.hover_item !== null)
            ev.target.insertBefore(element, DragAndDropHelper.hover_item);
        else
            ev.target.appendChild(element);
    }

    this.arrange = function(ev, node) {
        if (DragAndDropHelper.hover_item !== null) {
            var target = this.getValidTarget(DragAndDropHelper.hover_item);
            if (target !== null && target !== undefined) {
                target.parentElement.insertBefore(node, DragAndDropHelper.hover_item);
                return;
            }
        }

        ev.target.appendChild(node);

    }

    this.getValidTarget = function(target) {
        var lTarget = target;
        while ((lTarget !== null && lTarget !== undefined) && (!lTarget.className.includes(this.itemClassname))) {
            lTarget = lTarget.parentElement;
        }
        return lTarget;
    }

    this.replace = function(ev, element) {
        var target = this.getValidTarget(ev.target);
        if (target !== null)
            this.dropContainer.replaceChild(element, target);
    }

    this.dropContainer.addEventListener("drop", this.drop.bind(this), false);
    this.dropContainer.addEventListener("dragover", this.allowDrop.bind(this), false);

    {
        var _childs = document.getElementsByClassName(this.itemClassname);
        var _l = _childs.length;
        var _i = 0;

        for (_i = 0; _i < _l; _i++) {
            var child = _childs.item(_i);
            if (DragAndDropHelper.registered_ids.indexOf(child.id) === -1) {
                child.addEventListener("dragstart", function(e) { this.drag(e); }.bind(this), false);
                child.addEventListener("dragend", function(e) { this.resetDrag(e); }.bind(this), false);
                DragAndDropHelper.registered_ids.push(child.id);
            }
        }
    }
}

function initDnDContainer(container, classname) {
    new DragAndDropHelper(container, classname);
}