# Layout De Cores E Identidade Visual

## Direcao Visual

Criar uma identidade visual feminina, delicada e moderna, inspirada em uma menina de 15 anos, com aparencia beneficente, alegre e confiavel.

O visual deve ser leve, acolhedor e celebrativo, sem parecer infantil demais. A interface precisa transmitir carinho, organizacao e seguranca para quem esta contribuindo com a rifa.

## Paleta Principal

| Uso | Cor | Hex |
| --- | --- | --- |
| Fundo principal | Rosa quase branco | `#FFF8FA` |
| Superficie | Branco | `#FFFFFF` |
| Rosa claro | Rosa delicado | `#FADADD` |
| Cor primaria | Rosa principal | `#F48FB1` |
| Cor secundaria | Lilas suave | `#C8A2C8` |
| Destaque forte | Roxo | `#8E44AD` |
| Detalhe especial | Dourado suave | `#D4AF37` |
| Texto principal | Cinza escuro | `#4A4A4A` |
| Texto secundario | Cinza medio | `#777777` |

## Cores De Status

| Status | Uso | Hex |
| --- | --- | --- |
| Sucesso | Pago, confirmado | `#A8E6CF` |
| Aviso | Pendente, aguardando | `#FFE082` |
| Perigo | Expirado, erro | `#FFABAB` |
| Neutro | Cancelado, indisponivel | `#E5E5E5` |
| Reservado | Reserva temporaria | `#E9D7F0` |

## Tokens Visuais

```ts
export const theme = {
  colors: {
    background: '#FFF8FA',
    surface: '#FFFFFF',
    primary: '#F48FB1',
    primaryLight: '#FADADD',
    secondary: '#C8A2C8',
    accent: '#D4AF37',
    highlight: '#8E44AD',
    text: '#4A4A4A',
    muted: '#777777',
    success: '#A8E6CF',
    warning: '#FFE082',
    danger: '#FFABAB',
    neutral: '#E5E5E5',
    reserved: '#E9D7F0',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px',
  },
  borderRadius: {
    sm: '6px',
    md: '8px',
    lg: '12px',
    pill: '999px',
  },
  shadows: {
    soft: '0 6px 18px rgba(74, 74, 74, 0.08)',
    card: '0 10px 28px rgba(244, 143, 177, 0.16)',
  },
  fontSizes: {
    xs: '12px',
    sm: '14px',
    md: '16px',
    lg: '20px',
    xl: '28px',
    xxl: '36px',
  },
}
```

## Estilo Geral

- Layout limpo, delicado e responsivo.
- Design mobile first.
- Container maximo de `1100px`.
- Bordas arredondadas sem exagero.
- Cards com sombra suave.
- Botoes grandes e faceis de tocar no celular.
- Tipografia moderna, amigavel e legivel.
- Pequenos detalhes em dourado para sensacao de celebracao.
- Evitar excesso de roxo e evitar visual infantil.
- Evitar textos muito longos dentro de cards pequenos.

## Componentes

### BaseLayout

- Header simples com nome da rifa.
- Conteudo centralizado.
- Footer com mensagem beneficente.
- Fundo geral `#FFF8FA`.

### RaffleHero

- Banner principal com imagem da rifa.
- Titulo claro e emocional.
- Descricao curta.
- Botao principal: "Escolher meus numeros".
- Pode usar detalhe dourado discreto em selo, borda ou icone.

### RaffleInfoCard

- Valor por numero.
- Data do sorteio.
- Total de numeros.
- Quantidade vendida.
- Progresso da campanha.

### NumberGrid

Estados dos numeros:

- Disponivel: fundo branco, borda rosa, texto cinza.
- Selecionado: fundo rosa principal, texto branco.
- Reservado: fundo lilas claro, texto cinza, bloqueado.
- Pago: fundo cinza claro, texto secundario, bloqueado.
- Indisponivel: opacidade reduzida e cursor bloqueado.

### BuyerForm

Campos:

- Primeiro nome.
- Sobrenome.
- E-mail.
- Celular.

Requisitos visuais:

- Inputs arredondados.
- Label clara.
- Borda suave.
- Estado de erro.
- Estado de sucesso quando fizer sentido.

### CheckoutSummary

- Lista de numeros escolhidos.
- Valor total destacado.
- Dados do comprador.
- Botao para gerar pagamento.

### PaymentPixCard

- QR Code Pix.
- Codigo copia e cola.
- Botao copiar codigo.
- Status do pagamento.
- Mensagem curta explicando o prazo da reserva.

### ConfirmationCard

- Mensagem de agradecimento.
- Nome do comprador.
- Numeros comprados.
- Status da compra.
- Destaque visual delicado para celebracao.

### BaseButton

Variantes:

- `primary`: fundo rosa principal.
- `secondary`: fundo lilas.
- `outline`: borda rosa e fundo transparente.
- `gold`: dourado suave para acoes especiais.

Estados:

- Normal.
- Hover.
- Focus visivel.
- Disabled.
- Loading.

### BaseCard

- Fundo branco.
- Borda arredondada.
- Sombra leve.
- Espacamento confortavel.
- Sem cards aninhados.

### BaseInput

- Label clara.
- Campo arredondado.
- Borda suave.
- Estado de erro.
- Estado de sucesso.
- Mensagem auxiliar curta.

### StatusBadge

Variantes:

- `pending`: amarelo suave.
- `reserved`: lilas.
- `paid`: verde suave.
- `canceled`: cinza.
- `expired`: vermelho suave.

## Layout Responsivo

- Mobile first.
- Grid de numeros deve caber bem em telas pequenas.
- Em desktop, usar duas colunas quando fizer sentido: conteudo principal e resumo.
- Header fixo e opcional.
- Footer simples.
- Espacamento generoso, mas sem desperdiçar tela no celular.

## Acessibilidade

- Contraste suficiente entre texto e fundo.
- Estados visuais nao devem depender apenas de cor.
- Botoes devem ter foco visivel.
- Inputs devem ter label associada.
- Numeros bloqueados devem ter estado `disabled`.
- Mensagens de erro devem ser claras e curtas.

## Exemplo De Classes CSS Globais

```css
:root {
  --color-background: #FFF8FA;
  --color-surface: #FFFFFF;
  --color-primary: #F48FB1;
  --color-primary-light: #FADADD;
  --color-secondary: #C8A2C8;
  --color-accent: #D4AF37;
  --color-highlight: #8E44AD;
  --color-text: #4A4A4A;
  --color-muted: #777777;
  --color-success: #A8E6CF;
  --color-warning: #FFE082;
  --color-danger: #FFABAB;
  --radius-md: 8px;
  --shadow-card: 0 10px 28px rgba(244, 143, 177, 0.16);
}

body {
  background: var(--color-background);
  color: var(--color-text);
}
```
