# Selling a course or membership from Iceland: platforms, fees and who can pay an Icelandic seller

Built 2026-09-20 from main-pc, from the vendors' own pricing, help and terms
pages. Every quotation was seen in the page text; the `plat-*` claims in
`claims.json` re-check them. Facts only. The constraint that decides
everything: Stripe does not list Iceland, so a platform that makes the seller
connect his own Stripe account cannot pay him; a platform that collects the
money itself and pays out to a bank account can. Prices change often; the date
is part of every figure. "Merchant of record" means the platform is the legal
seller to the customer and carries the VAT duty in the customer's country.

## 1. Platforms that state they can pay a seller in Iceland

| Item | Value | Label | Source |
|---|---|---|---|
| Teachable | Iceland is in the supported-country list of its own payment gateway ("Hong Kong Hungary Iceland India Indonesia"); "Your earnings are paid directly to your bank account via Stripe", through an account Teachable sets up, not the seller's own; it "Handles U.S. sales tax, EU/UK VAT, and more."; "Starter Basic tools for getting your business started $39 /mo Billed monthly" with a "7.5% transaction fee", "Builder Essential features to build your multi-product offering $89 /mo Billed monthly" with none; "International credit & debit card sales 3.9% + 30¢"; video hosting included | [V 2026-09-20] | support.teachable.com/en/articles/11682555-teachable-payments; teachable.com/pricing |
| Skool (community with courses) | payout countries include "Hong Kong, Hungary, Iceland, India,"; "This is because Skool is a “merchant of record.”"; "Hobby $9/month Unlimited members Unlimited courses Unlimited videos Unlimited live calls 10% transaction fee" or "Pro $99/month Unlimited members Unlimited courses Unlimited videos Unlimited live calls 2.9% transaction fee"; "All subscription prices on Skool are in USD." and "Payouts are in your local currency. We do not support USD deposits outside of the US." | [V 2026-09-20] | help.skool.com/article/86-subscriptions-faq; skool.com/pricing |
| Gumroad | no monthly fee; "10% + $0.50 Per transaction for all sales through your profile or direct links to your customers."; "We're becoming your merchant of record, which means Gumroad will automatically handle all sales tax collection and remittance worldwide."; bank payouts list "Hungary HUF Iceland EUR India INR" - paid in euro, not króna; memberships supported | [V 2026-09-20] | gumroad.com/pricing; gumroad.com/help/article/13-getting-paid |
| Lemon Squeezy | merchant of record; "ecommerce 5% + 50¢", plus "+1.5% for international (outside of the US) transactions +1.5% for PayPal transactions +0.5% for subscription payments" and "1% per payout for bank accounts outside the US"; Iceland is in its bank-payout list ("Hong Kong Hungary Iceland India"). Its own 2026 note says it is moving users to a Stripe product where "Today Managed Payments support merchants in 35+ countries" - a continuity risk for a seller in Iceland [I] | [V 2026-09-20]; the risk [I] | lemonsqueezy.com/pricing; docs.lemonsqueezy.com (fees; supported-countries); lemonsqueezy.com/blog/2026-update |
| Paddle (checkout for one's own site) | merchant of record; "5% + 50¢ per Checkout transaction"; "Paddle works with software businesses anywhere in the world with the exception of the unsupported countries listed below." (Iceland is not on that list); "You can receive your payment either via wire transfer or Payoneer." Its rules say "Paddle is built to serve software companies (including B2B SaaS, Consumer Software, and Games)." while its marketing says "Scale your e-books, courses and downloadable files to sell anywhere in the world with Paddle as your Merchant of Record." - the two pages conflict; ask before building on it | [V 2026-09-20] | paddle.com/pricing; paddle.com/help |
| Patreon | "you are on our standard 10% pricing plan" plus "Credit card / Apple Pay Any 2.9% + $0.30"; bank payout list has "Belgium EUR Iceland EUR Benin XOF" | [V 2026-09-20] | support.patreon.com (creator fees; payouts outside the US) |
| YouTube | Iceland is listed for the Partner Programme and for channel memberships ("Hong Kong Hungary Iceland India"); memberships open at "500 subscribers with 3 valid public uploads in the last 90 days, and 3,000 qualified watch hours in the last 12 months"; full monetisation at "1,000 subscribers with 4,000 qualified watch hours in the last 12 months"; "YouTube will pay them 70% of net revenues from channel memberships, Super Chat, Super Stickers, and Super Thanks" | [V 2026-09-20] | support.google.com/youtube/answer/7101720; /13429240; /72851; /72902 |
| Udemy (marketplace) | "instructors receive 97% of the revenue when the student purchases their content using an instructor’s coupon or referral link" and "instructors receive 37% of the revenue for any Udemy sales where no instructor coupon or course referral link was used"; paid by PayPal or Payoneer; no country list published [G] | [V 2026-09-20]; Iceland [G] | support.udemy.com (instructor revenue share; payment overview) |

## 2. Platforms that cannot, or only in part

| Item | Value | Label | Source |
|---|---|---|---|
| Stripe itself | its country list runs "Ireland Italy Japan Kenya Extended network Latvia Liechtenstein" - no Iceland | [V 2026-09-20] | stripe.com/global |
| Thinkific | Iceland is absent from its own payments list ("Greece Hong Kong Hungary Ireland Italy Latvia"); the fallback is the seller's own Stripe, or PayPal, and "Our native PayPal integration does not offer support for recurring payment types (subscriptions and monthly payment plans)." | [V 2026-09-20] | support.thinkific.com (supported countries; Thinkific Payments, Stripe and PayPal) |
| Kajabi | its European payments list is euro countries only: "Currently supported countries: Austria Belgium Croatia Cyprus Estonia Finland France Germany Greece Ireland Italy Latvia Lithuania Luxembourg Malta Netherlands Portugal Slovakia Slovenia Spain"; from "$143 $179 /mo * Billed annually ($179/mo)" | [V 2026-09-20] | help.kajabi.com; kajabi.com/pricing |
| Podia | the seller connects his own processor, and "PayPal can be used for one-time payments only. It doesn’t support payment plans or subscription pricing." | [V 2026-09-20] | help.podia.com/en/articles/11321953 |
| Circle | paywalls need the seller's own Stripe account: "Choose the country where your Stripe account is registered or where you intend to register your Stripe account." | [V 2026-09-20] | help.circle.so |
| Freemius (already used for HelmCNC) | software only: "Freemius is exclusively focused on serving makers selling software like SaaS and downloadable software." A calculator app fits; a course does not | [V 2026-09-20] | freemius.com/help, allowed and prohibited products |
| Whop | "2.7% + $0.30 per successful transaction for domestic cards + 1.5% for international cards + 1% if currency conversion applies"; tax handling is an add-on at "2% per transaction (when enabled and tax is collected)"; payouts "in over 200 countries" with no country list, so Iceland is not confirmed [G] | [V 2026-09-20]; Iceland [G] | docs.whop.com/fees; payout methods |

## 3. Hosting the video oneself, and getting paid directly

| Item | Value | Label | Source |
|---|---|---|---|
| Cloudflare Stream (he already has a Cloudflare account) | "$5 per month for each 1,000 minutes of video storage capacity" and "billed at $1 per 1,000 minutes delivered"; additional audio tracks and captions are documented features | [V 2026-09-20] | developers.cloudflare.com/stream/pricing/ |
| Bunny Stream | "Bunny Stream Encoding Free Storage From $0.01/GB CDN From $0.005/GB" | [V 2026-09-20] | bunny.net/pricing/stream/ |
| Vimeo | hosting only on these plans; "bandwidth limit on our self-serve accounts to 2 TB (2,000 GB) per month" | [V 2026-09-20] | vimeo.com/upgrade-plan |
| PayPal business account in Iceland | exists; receiving commercial payments: "HR, IS, & MC EEA 3.40% + fixed fee UK 4.69% + fixed fee All other markets 5.39% + fixed fee" | [V 2026-09-20] | paypal.com/is/business/paypal-business-fees |
| Wise | individuals in Iceland can hold money ("Hong Kong*, Hungary Iceland, Ireland"); for a company, "When you add your details, we’ll let you know if we support businesses in your country." | [V 2026-09-20] | wise.com/help |

## 4. Why merchant of record matters (the VAT rule)

| Item | Value | Label | Source |
|---|---|---|---|
| Where a digital sale to a consumer is taxed | "B2C supplies of telecommunications , broadcasting and electronic services are taxed where the customer resides (Article 58 VAT Directive)" | [V 2026-09-20] | taxation-customs.ec.europa.eu, place of taxation |
| A platform that takes part in the sale is treated as the seller | "a taxable person taking part in that supply shall be presumed to be acting in his own name but on behalf of the provider of those services" | [V 2026-09-20] | eur-lex.europa.eu, Implementing Regulation 1042/2013, art. 9a |

## 5. What the facts allow [I]

- Four routes are open from Iceland today without a foreign company:
  Teachable (course site with tax handled), Skool (community, merchant of
  record), Gumroad and Lemon Squeezy (checkout only, merchant of record), and
  YouTube memberships once the channel passes 500 subscribers.
- A pre-sale needs only a checkout, not a course platform: Gumroad has no
  monthly fee and pays Iceland in euro; its price is 10 % of each sale.
- Per sale, the cheapest complete route found is Teachable's 89-dollar plan
  (no platform fee, card fee 3.9 % + 30 cents) once sales are steady; below
  roughly a thousand dollars a month the fee-only routes cost less than a
  monthly plan. That crossover is arithmetic on the list prices above, not a
  recommendation.
- The calculator app can go through Freemius, which already pays him; the
  course cannot.
- Building on his own site with Cloudflare Stream keeps the customer list and
  costs cents per student-hour, but then he needs a merchant of record for the
  checkout (Paddle's stance on courses is unclear; Lemon Squeezy's future for
  Iceland is uncertain).
