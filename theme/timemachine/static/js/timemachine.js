var Timemachine = new Class({
    Implements: [Options, Events],
    
    $pages:{},
    
    options: {
        
    },
    
    initialize: function(){
        this.$build();
    },
    
    $build: function(){
        var self = this,
            zindex = 1000,
            pages = $$('.page').reverse(),
            front = -1;
        
        this.container = document.getElement('.page_container');
        this.deck = new Deck.TimeMachine(this.container, {
            card_width: 110,
            zindex: 1000,
            'onCardMove': function(){
                this.cards.setStyle('box-shadow', 'none');
                this.cards[this.active].setStyle('box-shadow', '0px 1px 8px 2px rgba(0,0,0,.2)');
            }
        });

        this.request = new Request.JSON({
            'method': 'get',
            'onComplete': function(resp){
                self.$addPage(resp);
            }
        });
        
        pages.setStyles(self.deck.cardStyle(self.deck.cards.length)).each(function(page, i){
            self.deck.addCard(page, i, false, false);
        });

        window.addEvent('click:relay(a:not([href=#], [href^=http://], [href^=https://], [data-noxhr]))', function(e){
            e.stop();
            History.push(this.get('href'));
        });
        
        History.addEvent('change', function(){
            var path = window.location.pathname !== '/' ? window.location.pathname : '/index';

            self.$goToPage(path);
        });
    },
    
    $goToPage: function(uri){
        var idx = this.deck.findByName(uri);
        
        if(idx > -1){
            this.deck.toCard(idx);
        }else{
            this.request.setOptions({
                'url': uri
            }).send();
        }
        
        return this;
    },
    
    $addPage: function(data){
        var temp = new Element('div').set('html', data.content),
            div = temp.getElement('*:first-child');
            
        if(div){
            div.setStyles(this.deck.cardStyle(-1))
                .inject(this.container, 'top');
        
            this.deck.addCard(div, this.deck.active, data.path, true);
        }
        
        return this;
    }
});