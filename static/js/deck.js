var Deck = new Class({
    active: 0,
    previous: 0,
    Implements: [Options, Events],
    
    options: {
        /*onBuild: function(){},
        onCardIn: function(index){},
        onCardOut: function(index){},
        onCardStyle: function(index, style){},
        onCardAdded: function(index, card){},
        onCardRemoved: function(index, card){},
        onLoopFirst function(){},
        onLoopLast: function(){},
        */
        zindex: 1000,
        start: 0,
        loop: false,
        cascade_delta: true,
        auto_layout: true,
        pages: $$()
    },
    
    initialize: function(container, options){
        this.container = $(container);
        
        this.setOptions(options);
        this.$build();
    },
    
    $build: function(){
        var self = this;
        this.cards = this.options.pages;
        this.active = this.options.start;
        this.previous = this.options.start;
        
        if(this.options.auto_layout){
            Array.each(this.cards, function(card, index){  
                card.setStyles(self.$getCardStyle(index));
            });
        }
        
        this.build();
        this.fireEvent('build');
        this.toCard(this.active);
        
        return this;
    },
    
    $cardIn: function(index){
        this.cardIn(index);
        this.fireEvent('cardIn', [index]);
        
        return this;
    },
    
    $cardOut: function(index){
        this.cardOut(index);
        this.fireEvent('cardOut', [index]);
        
        return this;
    },
    
    $getCardStyle: function(index){
        var style = this.cardStyle(index) || {};
        
        this.fireEvent('cardStyle', [index, style]);
        
        return style;
    },
    
    $moveAllCards: function(from, direction){      
        var start = this.cards.length - 1,
            end = direction === 'forward' ? from : 0,
            action = direction === 'forward' ? '$cardIn' : '$cardOut';
        
        for(var x = start; x >= end; x--){
            if(x < this.active){
                this[action](x);
            }else{
                var style = this.$getCardStyle(x);
                console.log(x, style)
                this.cardMove(x, style);
            }
        }
        
        return this;
    },
    
    build: function(){
        return this;
    },

    cardStyle: function(index){
        return {}
    },

    cardIn: function(index){
        var card = this.cards[index];
        
        if(card){
            card.setStyle('display', 'block');
        }
        
        return this;
    },

    cardOut: function(index){
        var card = this.cards[index];

        if(card){
            card.setStyle('display', 'none');
        }
        
        return this;
    },

    cardMove: function(index, style){
        return this;
    },
    
    toCard: function(index){
        if(index !== this.active){
            var direction = index < this.active ? 'forward' : 'backward';
            
            if(direction === 'forward'){
                this.$cardOut(this.active);
            }else{
                this.$cardIn(index);
            } 
            
            this.previous = this.active;
            this.active = index;
            
            if(this.options.cascade_delta){
                this.$moveAllCards(index, direction);
            }           
            
            this.fireEvent('toCard', [index, direction]);
            
            if(index === 0){
                this.fireEvent('first');
            }
            
            if(index === this.cards.length - 1){
                this.fireEvent('last');
            }
        }
        
        return this;
    },
    
    findByName: function(name){
        var i = -1;
                 
        for(var x = 0, l = this.cards.length; x < l; x++){
            if(this.cards[x].get('data-name') === name){
                i = x;
                break;
            }
        }
        
        return i;
    },
    
    nextCard: function(){
        var next = this.active - 1 > -1 
            ? this.active - 1 
            : this.options.loop
                ? this.cards.length - 1
                : 0;
                
        if((this.active + 1) === this.cards.length){
            this.fireEvent('onLoopLast');
        }
        
        return this.toCard(next);
    },
    
    previousCard: function(){
        var previous = this.active + 1 < this.cards.length 
            ? this.active + 1 
            : this.options.loop
                ? 0
                : this.active;
        
        if((this.active - 1) === 0){
            this.fireEvent('onLoopFirst');
        }
        
        return this.toCard(previous);
    },
    
    addCard: function(card, position, name){
        name = name || 'new_card_'+ this.cards.length;
        var element,
            pos = position;
        
        switch(typeOf(card)){
            case 'function':
                element = card();
                break;
                
            case 'element':
                element = card;
                break;
                
            case 'string':
                element = new Element('div', {
                    'html': card
                });

                break;
        }
        
        if(position === 'first'){
            pos = 0;
            element.inject(this.cards[pos], 'before');
        }else if(position === 'last'){
            pos = this.cards.length;
            element.inject(this.contianer, 'bottom');
        }else if(isNaN(position)){
            pos = position;
            element.inject(this.cards[pos], 'before');
        }

        if(element.get('data-name')){
            name = element.get('data-name')
        }

        element.set('data-name', name);
        
        if(pos < this.active){
            this.active++;
        }
        
        this.cards.splice(pos, 0, element);
        this.fireEvent('cardAdded', [pos, card]);
        
        var style = this.$getCardStyle(pos);
        //console.log(element.get('data-name'), style, element.getStyles('*'))
        if(pos >= this.active){
            if(this.options.cascade_delta){
                var direction = pos < this.active ? 'forward' : 'backward';
                this.$moveAllCards(pos, direction);
            }
            
            this.cardMove(pos, style);
        }else{
            style['display'] = 'none';
            element.setStyles(style);
        }
        
        return this;
    },
    
    removeCard: function(index){
        if(this.cards[index]){
            this.cardOut(index);
            
            var card = this.cards.splice(index, 1);
            
            this.$moveAllCards(index, index > this.active ? 'forward' : 'backward');
            this.fireEvent('cardRemoved', [index, card]);
        }
        
        return this;
    }
});

Deck.TimeMachine = new Class({
    Extends: Deck,
    
    cardStyle: function(index){
        var diff = this.active - index,
            width = this.options.card_width + (diff * 5),
            style = {};

        if(diff < -3 && 7 == 8){
            style = {
                'z-index': this.options.zindex + diff,
                width: '90%',
                left: '5%',
                top: '-7%',
                height: '100%',
                opacity: 1
            };
        }else if(diff === 0){
            style = {            
                width: '110%',
                left: '-5%',
                height: '100%',
                top: '2%',
                'z-index': this.options.zindex += 1,
                opacity: 1,
                height: '100%'
            };
        }else if(diff > 0){
            style = {
                width: '115%',
                left: '-7.5%',
                height: '105%',
                opacity: 0,
                top: '0%',
                'z-index': this.options.zindex + this.cards.length
            };
        }else{
            style = {
                'z-index': this.options.zindex + diff,
                width: width + '%',
                left: ((100 - width) / 2) + '%',
                top: diff * 2 + 1 + '%',
                height: '100%',
                opacity: 1 + (diff / 10)
            };
            console.log('dd', 1 - (diff / 100))
        }

        return style;
    },
    
    cardIn: function(index){
        var card = this.cards[index],
            fx = card.get('morph'),
            style = this.cardStyle(this.previous); 

        fx.setOptions({
            unit: '%',
            duration: 500
        });

        card.setStyles({
            'display': 'block'
        });
        
        fx.start(style);
    },
    
    cardOut: function(index){
        var card = this.cards[index],
            fx = card.get('morph'),
            style = this.cardStyle(-1); 

        fx.setOptions({
            unit: '%',
            duration: 500
        });

        card.setStyle('display', 'block');
        fx.start(style).chain(function(){
            card.setStyle('display', 'none');
        });
    },
    
    cardMove: function(index, style){
        var card = this.cards[index],
            fx = card.get('morph'),
            update_index = function(){
                if(style['z-index']){
                    card.setStyle('z-index', style['z-index']);
                }
            };
        
        fx.setOptions({
            unit: '%',
            duration: 500
        });

        card.setStyle('display', 'block');

        if(index < this.active || index < this.previous){
            update_index();
        }

        fx.start(style).chain(function(){
            update_index();
        });
    }
});