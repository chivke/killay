/* 
  Video Sequence Engine
  ---------------------
  Require $player const with plyr obj.
*/

class SequenceEngine {
  constructor (
    {
      player = new Plyr('#player', {invertTime: false}),
      data_id = "sequences-data",
      menu_id = "sequences-menu",
      display_id = "sequences-display",
      display_title_id = "sequences-display-title",
      display_content_id = "sequences-display-content",
      player_id = "player",
      debug = false,
    } = {}
  ) {
    this.data_element = document.getElementById(data_id);
    this.menu_element = document.getElementById(menu_id);
    this.display_title_element = document.getElementById(display_title_id);
    this.display_content_element = document.getElementById(display_content_id);
    this.sequences_data = {};
    this.debug = debug;
    this._current_second = 0;
    this._load_sequences_data();
    $player.on("timeupdate", this.callback_timeupdate.bind(this));
  }

  get sequence_ids () {return Object.keys(this.sequences_data)}

  get last_sequence () {return this.sequences_data[this.last_sequence_id]}

  get_sequence_by_id (id) {return this.sequences_data[id]}

  get_sequence_by_value_field ({field, value}={}) {
    for (let i = 0; i < this.sequence_ids.length; i++) {
      let sequence = this.get_sequence_by_id(this.sequence_ids[i]);
      if (sequence[field] == value) {
        return sequence;
      }
    }
  }

  get_sequence_by_time (second) {
    for (let i = 0; i < this.sequence_ids.length; i++) {
      let sequence_id = this.sequence_ids[i];
      let sequence = this.get_sequence_by_id(this.sequence_ids[i]);
      if (sequence && this.is_time_in_sequence(second, sequence)) {
        return sequence;
      }
    }
  }

  get_sequence_by_order (value) {
    return this.get_sequence_by_value_field({field:"order", value});
  }

  is_time_in_sequence (second, sequence) {
    if (second >= sequence.ini && second < sequence.end) {return true;}
    else {return false}
  }
  
  _debug(log) {this.debug ? console.log(log): null}

  _load_sequences_data () {
    let sequences_lenght = this.data_element.children.length;
    this._debug(`loading sequences data (${sequences_lenght})`);
    for (let i = 0; i < sequences_lenght; i++) {
      let sequence_element = this.data_element.children[i];
      let sequence = this._get_sequence_obj_from_element(sequence_element);
      this.sequences_data[sequence.id] = sequence;
      if (i + 1 == this.data_element.children.length) {
        this.last_sequence_id = sequence.id;
        this.last_sequence_second = sequence.end;
      }
      this._create_selector_in_menu(sequence);
    }
  }

  _get_sequence_obj_from_element (element) {
    return {
      id: element.getAttribute("id"),
      order: parseInt(element.getAttribute("order")),
      ini: parseInt(element.getAttribute("ini")),
      end: parseInt(element.getAttribute("end")),
      title: element.children.namedItem("sequence-data-title").textContent,
      content: element.children.namedItem("sequence-data-content").cloneNode(true),
      selector: null,
    }
  }

  _create_selector_in_menu (sequence) {
    let selector = document.createElement("a");
    selector.setAttribute("class", "item");
    selector.setAttribute("id", sequence.id);
    selector.setAttribute("ini", sequence.ini);
    selector.setAttribute("end", sequence.end);
    selector.onclick = this.callback_select_sequence_onclick.bind(this);
    selector.appendChild(
      document.createTextNode(sequence.order)
    );
    sequence.selector = selector;
    this.menu_element.appendChild(selector);
    return selector;
  }

  clean_sequence_selectors () {
    for (let i = 0; i < this.menu_element.children.length; i++) {
      let sequence_selector =  this.menu_element.children[i];
      sequence_selector.setAttribute("class", "item");
    }
  }

  clean_sequence_display () {
    this.display_title_element.textContent = "";
    this.display_content_element.textContent = "";
  }

  select_sequence (sequence) {
    this.clean_sequence_selectors();
    this.current_sequence = sequence;
    sequence.selector.setAttribute("class", "item active");
    this.display_sequence(sequence);
    this._debug(`sequence ${sequence.order} manual selected`);
  }

  display_sequence (sequence) {
    let current_second = parseInt($player.currentTime);
    if (current_second != sequence.ini) {
      $player.currentTime = sequence.ini;
    }
    this.clean_sequence_display();
    this.display_title_element.appendChild(document.createTextNode(sequence.title));
    this.display_content_element.appendChild(sequence.content);
    $player.play();
  }

  callback_select_sequence_onclick (event) {
    let sequence_selector = event.target;
    //sequence_selector.setAttribute("class", "item active");
    let sequence_id = sequence_selector.getAttribute("id");
    let sequence = this.get_sequence_by_id(sequence_id)
    this.select_sequence(sequence);
  }

  select_sequence_by_time (second) {
    let sequence = this.get_sequence_by_time(second);
    sequence ? this._debug(`sequence ${sequence.order} founded by time: ${second}s`): null;
    return sequence ? this.select_sequence(sequence) : null;
  }

  callback_timeupdate (event) {
    let current_second = parseInt($player.currentTime);
    if (this._current_second == current_second) {return}
    this._current_second = current_second;
    this._debug(`current second: ${current_second} [${$player.currentTime}]`);
    // search initial sequence
    if (!this.current_sequence) {
      this._debug("current sequence not founded")
      return this.select_sequence_by_time(current_second);
    }
    // if time is in the current sequence
    if (
      this.current_sequence && this.is_time_in_sequence(current_second, this.current_sequence)
    ) {
      this._debug(`current time (${current_second}s) in sequence ${this.current_sequence.order}`)
      return
    } // do nothing

    // if is out of last sequence
    if (current_second > this.last_sequence_second) {
      // verify if last sequence is selected
      this._debug(`curren time (${current_second}s) out of sequences (>${this.last_sequence_second}s)`);
      if (this.current_sequence.id != this.last_sequence_id) {this.select_sequence(this.last_sequence);}
      return
    }

    // if time is in the next sequence
    let next_sequence = this.get_sequence_by_order(this.current_sequence.order + 1);
    if (next_sequence && this.is_time_in_sequence(current_second, next_sequence)) {
      this._debug(`change sequence ${this.current_sequence.order} to de next sequence ${next_sequence.order}`);
      this.select_sequence(next_sequence); // set next
      return
    }

    // search for sequence
    this._debug(`searching sequence for current time (${current_second}s)`)
    let founded_sequence = this.get_sequence_by_time(current_second);
    return founded_sequence ? this.select_sequence(founded_sequence): null;
  }
}
